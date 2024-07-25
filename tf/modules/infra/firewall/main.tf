# Entrypoint for the firewall module.

# The firewall and its bucket needs to reside in us-east-1 as the WAF is scoped
# to Cloudfront which can only exist in us-east-1. Even if we are, in fact,
# actually deploying everything in us-east-1 its better just to make it
# explicit in case that fact changes at some point in the future.
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

module "waf_logs" {
  source = "../..//_reusable/bucket/"

  # This is a Cloudfront scoped WAF so make sure all the resources in the
  # module use the correct provider.
  providers = {
    aws = aws.acm
  }

  acl                      = "log-delivery-write"
  aws_account              = var.aws_account
  control_object_ownership = true
  environment              = var.environment
  force_destroy            = var.force_destroy
  name                     = module.waf_logs_label.id
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
        days = var.lifecycle_rule.expiration_days
      }

      noncurrent_version_expiration = {
        noncurrent_days = var.lifecycle_rule.noncurrent_expiration_days
      }

      noncurrent_version_transition = {
        noncurrent_days = var.lifecycle_rule.noncurrent_transition_days
        storage_class   = var.lifecycle_rule.storage_class
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

module "waf" {
  source = "../..//_reusable/waf/"

  # This is a Cloudfront scoped WAF so make sure all the resources in the
  # module use the correct provider.
  providers = {
    aws = aws.acm
  }

  countries               = var.countries
  environment             = var.environment
  ipv4_ip_set_addresses   = var.ipv4_ip_set_addresses
  ipv6_ip_set_addresses   = var.ipv6_ip_set_addresses
  log_destination_configs = module.waf_logs.arn
  namespace               = var.namespace
  rules                   = var.rules
}
