# Inject the network module.

terraform {
  source = "../../../..//modules/infra/network/"
}

locals {
  env           = read_terragrunt_config(find_in_parent_folders("environment.hcl"))
  allowed_roles = local.env.locals.allowed_roles
  environment   = local.env.locals.environment
  ports         = local.env.locals.ports
}

inputs = {
  allowed_roles          = local.allowed_roles
  az_count               = 2
  cidr                   = "10.0.0.0/16"
  destination_cidr_block = "0.0.0.0/0"
  force_destroy          = contains(["staging"], local.environment)
  ssl_port               = local.ports.ssl
}
