# Inject the security module.

terraform {
  source = "../../../..//modules/infra/security/"
}

locals {
  env           = read_terragrunt_config(find_in_parent_folders("environment.hcl"))
  allowed_roles = local.env.locals.allowed_roles
}

inputs = {
  allowed_roles = local.allowed_roles
}
