# Entrypoint for the cdn module.

# Cloudfront needs to reside in us-east-1 so ensure that.
provider "aws" {
  alias  = "acm"
  region = "us-east-1"

  default_tags {
    tags = {
      Environment = var.environment
      Namespace   = var.namespace
    }
  }
}

locals {
  additional_domains    = slice(var.tenant_domains, 1, length(var.tenant_domains))
  allowed_methods       = ["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
  allowed_origins       = [for domain in var.tenant_domains : "https://${domain}"]
  origin_id_alb         = "${var.namespace}-${var.environment}-s3-origin-alb"
  origin_id_assets      = "${var.namespace}-${var.environment}-s3-origin-assets"
  origin_id_staticfiles = "${var.namespace}-${var.environment}-s3-origin-staticfiles"
}

# Buckets
module "access_logs" {
  source = "../..//_reusable/bucket/"

  acl                      = "log-delivery-write"
  aws_account              = var.aws_account
  control_object_ownership = true
  environment              = var.environment
  force_destroy            = var.force_destroy
  name                     = "cloudfront-logs"
  namespace                = var.namespace
  object_ownership         = "ObjectWriter"

  lifecycle_rule = [
    {
      id     = "ssm"
      status = "Enabled"

      filter = {
        prefix = "/"
      }

      expiration = {
        days = 90
      }

      noncurrent_version_expiration = {
        noncurrent_days = 90
      }

      noncurrent_version_transition = {
        noncurrent_days = 30
        storage_class   = "STANDARD_IA"
      }
    }
  ]

  server_side_encryption_configuration = {
    rule = {
      apply_server_side_encryption_by_default = {
        sse_algorithm = "AES256"
      }
      bucket_key_enabled = true
    }
  }

  versioning = {
    enabled = true
  }
}

# tfsec:ignore:aws-s3-block-public-policy tfsec:ignore:aws-s3-no-public-buckets
module "assets" {
  source = "../..//_reusable/bucket/"

  aws_account              = var.aws_account
  control_object_ownership = true
  environment              = var.environment
  force_destroy            = var.force_destroy
  name                     = "assets"
  namespace                = var.namespace
  object_ownership         = "BucketOwnerEnforced"

  logging = {
    target_bucket = module.access_logs.bucket_id
    target_prefix = "assets/"
  }

  server_side_encryption_configuration = {
    rule = {
      apply_server_side_encryption_by_default = {
        sse_algorithm = "AES256"
      }
      bucket_key_enabled = true
    }
  }

  versioning = {
    enabled = true
  }
}

module "staticfiles" {
  source = "../..//_reusable/bucket/"

  aws_account              = var.aws_account
  control_object_ownership = true
  environment              = var.environment
  force_destroy            = var.force_destroy
  name                     = "staticfiles"
  namespace                = var.namespace
  object_ownership         = "BucketOwnerEnforced"

  cors_rules = [
    {
      allowed_headers = ["*"]
      allowed_methods = ["GET"]
      allowed_origins = local.allowed_origins
      expose_headers  = ["ETag"]
      max_age_seconds = 3000
    },
  ]

  logging = {
    target_bucket = module.access_logs.bucket_id
    target_prefix = "staticfiles/"
  }

  server_side_encryption_configuration = {
    rule = {
      apply_server_side_encryption_by_default = {
        sse_algorithm = "AES256"
      }
      bucket_key_enabled = true
    }
  }

  versioning = {
    enabled = true
  }
}

# Distribution
resource "aws_cloudfront_origin_access_control" "s3" {
  name                              = module.cdn_oac_label.id
  description                       = "OAC for Cloudfront"
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}

resource "aws_cloudfront_function" "viewer_request" {
  name    = module.cloudfront_function_label_vr.id
  runtime = "cloudfront-js-1.0"
  publish = true
  code    = file("${path.module}/files/viewer-request.js")
}

module "cloudfront" {
  source = "../..//_reusable/cloudfront/"

  # Any Cloudfront distribution must be in us-east-1.
  providers = {
    aws = aws.acm
  }

  domain             = var.domain
  aliases            = var.tenant_domains
  additional_domains = local.additional_domains

  dns_ttl         = var.dns_ttl
  environment     = var.environment
  log_destination = "${module.access_logs.bucket_id}.s3.amazonaws.com"
  namespace       = var.namespace
  price_class     = var.price_class
  web_acl_id      = data.aws_wafv2_web_acl.this.arn

  origin = {
    alb = {
      domain_name = data.aws_lb.this.dns_name
      origin_id   = local.origin_id_alb

      custom_origin_config = {
        http_port              = 80
        https_port             = 443
        origin_protocol_policy = "match-viewer"
        origin_ssl_protocols   = ["TLSv1", "TLSv1.1", "TLSv1.2"]
      }
    }

    assets = {
      domain_name              = module.assets.bucket_regional_domain_name
      origin_id                = local.origin_id_assets
      origin_access_control_id = aws_cloudfront_origin_access_control.s3.id
    }

    staticfiles = {
      domain_name              = module.staticfiles.bucket_regional_domain_name
      origin_id                = local.origin_id_staticfiles
      origin_access_control_id = aws_cloudfront_origin_access_control.s3.id
    }
  }

  default_cache_behavior = {
    allowed_methods          = local.allowed_methods
    cached_methods           = ["GET", "HEAD"]
    cache_policy_id          = "4135ea2d-6df8-44a3-9df3-4b5a84be39ad" # CachingDisabled
    origin_request_policy_id = "216adef6-5c7f-47e4-b989-5492eafa07d3" # AllViewer
    target_origin_id         = local.origin_id_alb
    viewer_protocol_policy   = "redirect-to-https"
  }

  ordered_cache_behavior = [
    {
      path_pattern           = "/db*"
      allowed_methods        = local.allowed_methods
      cached_methods         = ["GET", "HEAD"]
      target_origin_id       = local.origin_id_assets
      viewer_protocol_policy = "redirect-to-https"

      forwarded_values = {
        query_string = true
        cookies = {
          forward = "all"
        }
      }

      function_association = [
        {
          event_type   = "viewer-request"
          function_arn = aws_cloudfront_function.viewer_request.arn
        }
      ]
    },
    {
      path_pattern           = "/media*"
      allowed_methods        = local.allowed_methods
      cached_methods         = ["GET", "HEAD"]
      cache_policy_id        = "658327ea-f89d-4fab-a63d-7e88639e58f6" # CachingOptimized
      target_origin_id       = local.origin_id_staticfiles
      viewer_protocol_policy = "redirect-to-https"
    },
    {
      path_pattern           = "/static*"
      allowed_methods        = local.allowed_methods
      cached_methods         = ["GET", "HEAD"]
      cache_policy_id        = "658327ea-f89d-4fab-a63d-7e88639e58f6" # CachingOptimized
      target_origin_id       = local.origin_id_staticfiles
      viewer_protocol_policy = "redirect-to-https"
    },
  ]
}

# DNS
resource "aws_route53_record" "www_a" {
  for_each = data.aws_route53_zone.tenant_zones
  zone_id  = each.value.zone_id
  name     = each.value.name
  type     = "A"

  alias {
    name                   = module.cloudfront.domain_name
    zone_id                = module.cloudfront.hosted_zone_id
    evaluate_target_health = false
  }
}

resource "aws_route53_record" "www_aaaa" {
  for_each = data.aws_route53_zone.tenant_zones
  zone_id  = each.value.zone_id
  name     = each.value.name
  type     = "AAAA"

  alias {
    name                   = module.cloudfront.domain_name
    zone_id                = module.cloudfront.hosted_zone_id
    evaluate_target_health = false
  }
}
