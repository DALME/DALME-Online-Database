# Inject the authorization module.

terraform {
  source = "../../../..//modules/infra/authorization/"
}

locals {
  env          = read_terragrunt_config(find_in_parent_folders("environment.hcl"))
  lock_table   = local.env.locals.lock_table
  allowed_oidc = local.env.locals.allowed_oidc
}

inputs = {
  lock_table   = local.lock_table
  allowed_oidc = local.allowed_oidc
}
