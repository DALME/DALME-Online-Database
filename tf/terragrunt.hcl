# https://terragrunt.gruntwork.io
# https://github.com/gruntwork-io/terragrunt
locals {
  env_vars           = read_terragrunt_config(find_in_parent_folders("env.hcl"))
  region_vars        = read_terragrunt_config(find_in_parent_folders("region.hcl"))
  aws_account        = local.env_vars.locals.aws_account
  environment        = local.env_vars.locals.environment
  gha_oidc_role_name = local.env_vars.locals.gha_oidc_role_name
  lock_table         = local.env_vars.locals.lock_table
  service            = local.env_vars.locals.service
  aws_region         = local.region_vars.locals.aws_region
}

# Generate an AWS provider block template.
generate "provider" {
  path      = "provider.tf"
  if_exists = "overwrite_terragrunt"
  contents  = <<EOF
# Workarounds for terragrunt's (current) inability to handle OIDC role chaining.
variable "oidc_session_name" {
  description = "The OIDC session name."
  type        = string
  default     = null
}

variable "oidc_web_identity_token" {
  description = "The OIDC session token."
  type        = string
  default     = null
}

# This will be the default provider.
# https://developer.hashicorp.com/terraform/language/providers/configuration#default-provider-configurations
provider "aws" {
  region = "${local.aws_region}"

  # Only these AWS Account IDs may be operated on by this template
  allowed_account_ids = ["${local.aws_account}"]

  dynamic "assume_role_with_web_identity" {
    for_each = var.oidc_web_identity_token == null ? {} : { oidc_enabled = true }

    content {
      role_arn                = "arn:aws:iam::${local.aws_account}:role/${local.gha_oidc_role_name}"
      session_name            = var.oidc_session_name
      web_identity_token      = var.oidc_web_identity_token
    }
  }

  # Ensure all resources have these common, project tags.
  default_tags {
    tags = {
      Environment = "${local.environment}"
      Service     = "${local.service}"
    }
  }
}

# Cloudfront also needs the us-east-1 provider so let's just alias it here and
# keep all provider details in the same location.
provider "aws" {
  alias  = "acm"
  region = "us-east-1" # NOTE: Region must be us-east-1 for Cloudfront etc.

  allowed_account_ids = ["${local.aws_account}"]

  default_tags {
    tags = {
      Environment = "${local.environment}"
      Service     = "${local.service}"
    }
  }
}
EOF
}

# Generate a modular remote state template.
remote_state {
  backend = "s3"

  disable_init = tobool(get_env("TF_DISABLE_INIT", "false"))

  config = {
    encrypt        = true
    bucket         = "${local.service}-tfstate-${local.environment}-${local.aws_account}"
    key            = "${path_relative_to_include()}/terraform.tfstate"
    region         = local.aws_region
    dynamodb_table = local.lock_table
  }

  generate = {
    path      = "backend.tf"
    if_exists = "overwrite"
  }
}

# Root-level variables.
# These variables apply to all configurations in this subfolder. They are
# pulled in by any module that needs them via an `include` block.
inputs = merge(
  local.env_vars.locals,
  local.region_vars.locals,
)
