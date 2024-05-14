# Root terragrunt configuration.
# https://github.com/gruntwork-io/terragrunt

locals {
  environment_vars   = read_terragrunt_config(find_in_parent_folders("environment.hcl"))
  region_vars        = read_terragrunt_config(find_in_parent_folders("region.hcl"))
  aws_account        = local.environment_vars.locals.aws_account
  environment        = local.environment_vars.locals.environment
  gha_oidc_role_name = local.environment_vars.locals.gha_oidc_role_name
  lock_table         = local.environment_vars.locals.lock_table
  namespace          = local.environment_vars.locals.namespace
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
      Namespace   = "${local.namespace}"
      Environment = "${local.environment}"
    }
  }
}
EOF
}

# Generate variable declarations that all modules require.
generate "metadata" {
  path      = "metadata.tf"
  if_exists = "overwrite_terragrunt"
  contents  = <<EOF
# tflint-ignore: terraform_unused_declarations
variable "aws_account" {
  description = "The AWS account where resources are created."
  type        = number
  default     = "${local.aws_account}"
}

# tflint-ignore: terraform_unused_declarations
variable "aws_region" {
  description = "The AWS region where resources are created."
  type        = string
  default     = "${local.aws_region}"
}

# tflint-ignore: terraform_unused_declarations
variable "environment" {
  description = "Identify the deployment environment."
  type        = string
  default     = "${local.environment}"
}

# tflint-ignore: terraform_unused_declarations
variable "namespace" {
  description = "The project namespace."
  type        = string
  default     = "${local.namespace}"
}
EOF
}

terraform {
  before_hook "before_hook" {
    commands = ["apply", "plan"]
    execute  = ["tflint"]
  }

  after_hook "init_lock_providers" {
    commands = ["init"]
    execute = [
      "terraform",
      "providers",
      "lock",
      "-platform=linux_amd64",
      "-platform=darwin_amd64",
      "-platform=darwin_arm64",
    ]
    run_on_error = false
  }

  after_hook "init_copy_back_lockfile" {
    commands     = ["init"]
    execute      = ["cp", ".terraform.lock.hcl", "${get_terragrunt_dir()}"]
    run_on_error = false
  }
}

# Generate a modular remote state template.
remote_state {
  backend = "s3"

  disable_init = tobool(get_env("TF_DISABLE_INIT", "false"))

  config = {
    encrypt        = true
    bucket         = "${local.namespace}-${local.environment}-tfstate-${local.aws_account}"
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
  local.environment_vars.locals,
  local.region_vars.locals,
)
