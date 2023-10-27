# Terraform definitions for the cloudfront module.

terraform {
  required_version = "~> 1.3"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.14.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "2.4.0"
    }
  }
}

// Certificate
locals {
  domain                      = var.tenant_domains[0]
  alt_domains                 = slice(var.tenant_domains, 1, length(var.tenant_domains))
  wildcard_domains            = [for domain in var.tenant_domains : "*.${domain}"]
  subject_alternative_domains = concat(local.alt_domains, local.wildcard_domains)
}

resource "aws_acm_certificate" "cloudfront" {
  domain_name               = local.domain
  subject_alternative_names = local.subject_alternative_domains
  provider                  = aws.acm
  validation_method         = "DNS"

  lifecycle {
    create_before_destroy = true
  }

  tags = {
    Name = "${var.service}-ssl-certificate-cloudfront-${var.environment}"
  }
}

data "aws_route53_zone" "tenant_zones" {
  for_each = toset(var.tenant_domains)
  name     = each.key
}

locals {
  zone_ids = {
    for zone in data.aws_route53_zone.tenant_zones : zone.name => zone.zone_id
  }
}

resource "aws_route53_record" "cloudfront" {
  for_each = {
    for dvo in aws_acm_certificate.cloudfront.domain_validation_options : dvo.domain_name => {
      name    = dvo.resource_record_name
      record  = dvo.resource_record_value
      type    = dvo.resource_record_type
      zone_id = local.zone_ids[dvo.domain_name]
    } if !strcontains(dvo.domain_name, "*.")
  }

  allow_overwrite = true
  name            = each.value.name
  records         = [each.value.record]
  ttl             = var.dns_ttl
  type            = each.value.type
  zone_id         = each.value.zone_id
}

resource "aws_acm_certificate_validation" "cloudfront" {
  certificate_arn = aws_acm_certificate.cloudfront.arn
  provider        = aws.acm
  validation_record_fqdns = [
    for record in aws_route53_record.cloudfront : record.fqdn
  ]
}

// Buckets
locals {
  assets          = "${var.service}-assets-${var.environment}-${var.aws_account}"
  static          = "${var.service}-staticfiles-${var.environment}-${var.aws_account}"
  logging         = "${var.service}-access-logs-cloudfront-${var.environment}-${var.aws_account}"
  allowed_origins = [for domain in var.tenant_domains : "https://${domain}"]
}

# tfsec:ignore:aws-s3-enable-bucket-encryption tfsec:ignore:aws-s3-encryption-customer-key
module "access_logs" {
  source  = "terraform-aws-modules/s3-bucket/aws"
  version = "3.15.1"

  bucket        = local.logging
  force_destroy = var.force_destroy

  acl                      = "log-delivery-write"
  control_object_ownership = true
  object_ownership         = "ObjectWriter"

  versioning = {
    enabled = true
  }

  tags = {
    Name = local.logging
  }
}

# tfsec:ignore:aws-s3-enable-bucket-encryption tfsec:ignore:aws-s3-encryption-customer-key
module "assets" {
  source  = "terraform-aws-modules/s3-bucket/aws"
  version = "3.15.1"

  bucket        = local.assets
  force_destroy = var.force_destroy

  control_object_ownership = true
  object_ownership         = "BucketOwnerEnforced"

  logging = {
    target_bucket = module.access_logs.s3_bucket_id
    target_prefix = "assets/"
  }

  versioning = {
    enabled = true
  }

  tags = {
    Name = local.assets
  }
}

# tfsec:ignore:aws-s3-enable-bucket-encryption tfsec:ignore:aws-s3-encryption-customer-key tfsec:ignore:aws-s3-block-public-policy tfsec:ignore:aws-s3-no-public-buckets
module "staticfiles" {
  source  = "terraform-aws-modules/s3-bucket/aws"
  version = "3.15.1"

  bucket        = local.static
  force_destroy = var.force_destroy

  control_object_ownership = true
  object_ownership         = "BucketOwnerEnforced"
  block_public_policy      = false
  restrict_public_buckets  = false

  cors_rule = [
    {
      allowed_headers = ["*"]
      allowed_methods = ["GET"]
      allowed_origins = local.allowed_origins
      expose_headers  = ["ETag"]
      max_age_seconds = 3000
    },
  ]

  logging = {
    target_bucket = module.access_logs.s3_bucket_id
    target_prefix = "staticfiles/"
  }

  versioning = {
    enabled = true
  }

  tags = {
    Name = local.static
  }
}

// Distribution
locals {
  origin_id             = "${var.service}-s3-origin-${var.environment}"
  assets_origin_id      = "${var.service}-s3-assets-origin-${var.environment}"
  staticfiles_origin_id = "${var.service}-s3-staticfiles-origin-${var.environment}"
}

resource "aws_cloudfront_origin_access_control" "s3" {
  name                              = "${var.service}-oac-cloudfront-s3-${var.environment}"
  description                       = "OAC for Cloudfront"
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}

resource "aws_cloudfront_distribution" "main" {
  aliases             = var.tenant_domains
  enabled             = true
  is_ipv6_enabled     = true
  wait_for_deployment = true
  web_acl_id          = var.web_acl_id

  # Cloudfront will fail on create unless the certificates are already validated.
  depends_on = [
    aws_acm_certificate_validation.cloudfront,
  ]

  logging_config {
    bucket          = "${module.access_logs.s3_bucket_id}.s3.amazonaws.com"
    prefix          = "cloudfront"
    include_cookies = false
  }

  origin {
    domain_name = var.alb_dns
    origin_id   = local.origin_id

    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "match-viewer"
      origin_ssl_protocols   = ["TLSv1.2"]
    }
  }

  origin {
    domain_name              = module.assets.s3_bucket_bucket_regional_domain_name
    origin_id                = local.assets_origin_id
    origin_access_control_id = aws_cloudfront_origin_access_control.s3.id
  }

  origin {
    domain_name              = module.staticfiles.s3_bucket_bucket_regional_domain_name
    origin_id                = local.staticfiles_origin_id
    origin_access_control_id = aws_cloudfront_origin_access_control.s3.id
  }

  default_cache_behavior {
    allowed_methods        = var.allowed_methods
    cached_methods         = ["GET", "HEAD"]
    target_origin_id       = local.origin_id
    viewer_protocol_policy = "redirect-to-https"

    default_ttl = 0
    min_ttl     = 0
    max_ttl     = 0

    forwarded_values {
      query_string = true
      headers      = ["*"]
      cookies {
        forward = "all"
      }
    }
  }

  ordered_cache_behavior {
    path_pattern           = "/db*"
    allowed_methods        = var.allowed_methods
    cached_methods         = ["GET", "HEAD"]
    target_origin_id       = local.assets_origin_id
    viewer_protocol_policy = "redirect-to-https"

    forwarded_values {
      query_string = true
      cookies {
        forward = "all"
      }
    }

    function_association {
      event_type   = "viewer-request"
      function_arn = aws_cloudfront_function.viewer_request.arn
    }
  }

  ordered_cache_behavior {
    path_pattern           = "/media*"
    allowed_methods        = var.allowed_methods
    cached_methods         = ["GET", "HEAD"]
    cache_policy_id        = "658327ea-f89d-4fab-a63d-7e88639e58f6" # CachingOptimized
    target_origin_id       = local.staticfiles_origin_id
    viewer_protocol_policy = "redirect-to-https"
  }

  ordered_cache_behavior {
    path_pattern           = "/static*"
    allowed_methods        = var.allowed_methods
    cached_methods         = ["GET", "HEAD"]
    cache_policy_id        = "658327ea-f89d-4fab-a63d-7e88639e58f6" # CachingOptimized
    target_origin_id       = local.staticfiles_origin_id
    viewer_protocol_policy = "redirect-to-https"
  }

  price_class = "PriceClass_100"

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    acm_certificate_arn      = aws_acm_certificate.cloudfront.arn
    minimum_protocol_version = "TLSv1.2_2021"
    ssl_support_method       = "sni-only"
  }

  tags = {
    Name = "${var.service}-cloudfront-${var.environment}"
  }
}

// Cloudfront Functions
resource "aws_cloudfront_function" "viewer_request" {
  name    = "${var.service}-cloudfront-function-viewer-request-${var.environment}"
  runtime = "cloudfront-js-1.0"
  publish = true
  code    = file("${path.module}/files/viewer-request.js")
}

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
