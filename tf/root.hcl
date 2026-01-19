# Root terragrunt configuration.
# https://github.com/gruntwork-io/terragrunt

locals {
  environment_vars = read_terragrunt_config(find_in_parent_folders("environment.hcl"))
  region_vars      = read_terragrunt_config(find_in_parent_folders("region.hcl"))

  aws_account = local.environment_vars.locals.aws_account
  aws_region  = local.region_vars.locals.aws_region

  aws_account_dns          = 203918846978 # The ida-root account.
  aws_dns_writer_role_name = local.environment_vars.locals.aws_dns_writer_role_name

  namespace   = local.environment_vars.locals.namespace
  environment = local.environment_vars.locals.environment
}

generate "provider" {
  path      = "provider.tf"
  if_exists = "overwrite_terragrunt"
  contents  = <<EOF
provider "aws" {
  region = "${local.aws_region}"
  allowed_account_ids = ["${local.aws_account}"]

  default_tags {
    tags = {
      Namespace   = "${local.namespace}"
      Environment = "${local.environment}"
    }
  }
}

provider "aws" {
  alias  = "acm"
  region = "us-east-1"
  allowed_account_ids = ["${local.aws_account}"]

  default_tags {
    tags = {
      Namespace   = "${local.namespace}"
      Environment = "${local.environment}"
    }
  }
}

provider "aws" {
  alias  = "dns_account"
  region = "${local.aws_region}"
  allowed_account_ids = ["${local.aws_account_dns}"]

  assume_role {
    role_arn = "arn:aws:iam::${local.aws_account_dns}:role/${local.aws_dns_writer_role_name}"
  }

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

remote_state {
  backend = "s3"

  disable_init = tobool(get_env("TF_DISABLE_INIT", "false"))

  config = {
    bucket       = "${local.namespace}-${local.environment}-tfstate-${local.aws_account}"
    encrypt      = true
    key          = "${path_relative_to_include()}/terraform.tfstate"
    region       = local.aws_region
    use_lockfile = true # Uses s3 native locking, no dynamodb necessary.
  }

  generate = {
    path      = "backend.tf"
    if_exists = "overwrite"
  }
}
