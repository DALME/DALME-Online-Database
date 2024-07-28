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
  origin_id             = "${var.namespace}-${var.environment}-s3-origin"
  alb_origin_id         = "${var.namespace}-${var.environment}-s3-origin-alb"
  staticfiles_origin_id = "${var.namespace}-${var.environment}-s3-origin-staticfiles"
  index                 = var.default_root_object
}

// Buckets
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

// Distribution
resource "aws_cloudfront_origin_access_control" "s3" {
  name                              = module.cloudfront_oac_label.id
  description                       = "OAC for Cloudfront"
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}

resource "aws_cloudfront_function" "viewer_request" {
  name    = "${var.service}-cloudfront-function-viewer-request-${var.environment}"
  runtime = "cloudfront-js-1.0"
  publish = true
  code    = file("${path.module}/files/viewer-request.js")
}

# module "cloudfront" {
#   source = "../..//_reusable/cloudfront/"

#   # Any Cloudfront distribution must be in us-east-1.
#   providers = {
#     aws = aws.acm
#   }

#   domain             = var.domain
#   additional_domains = local.additional_domains

#   aliases = var.tenant_domains
#   # default_root_object = "index.html"  # TODO: Don't think we need this.
#   dns_ttl         = var.dns_ttl
#   log_destination = "${module.access_logs.bucket_id}.s3.amazonaws.com"
#   namespace       = var.namespace
#   price_class     = var.price_class
#   web_acl_id      = data.aws_wafv2_web_acl.this.arn

# TODO: All origin config here.
# https://github.com/ocp/DALME-Online-Database/blob/74901dc7baff0655ca312d4dd05e6dfab2c62de6/tf/modules/cloudfront/main.tf#L202
# But bring up to spec with:
# https://github.com/SHARIAsource/ops-infra/blob/ocp/development/tf/modules/infra/cdn/main.tf
# }

// DNS
resource "aws_route53_record" "www-a" {
  for_each = data.aws_route53_zone.tenant_zones
  zone_id  = each.value.zone_id
  name     = each.value.name
  type     = "A"

  alias {
    name                   = aws_cloudfront_distribution.main.domain_name
    zone_id                = aws_cloudfront_distribution.main.hosted_zone_id
    evaluate_target_health = false
  }
}

resource "aws_route53_record" "www-aaaa" {
  for_each = data.aws_route53_zone.tenant_zones
  zone_id  = each.value.zone_id
  name     = each.value.name
  type     = "AAAA"

  alias {
    name                   = aws_cloudfront_distribution.main.domain_name
    zone_id                = aws_cloudfront_distribution.main.hosted_zone_id
    evaluate_target_health = false
  }
}
