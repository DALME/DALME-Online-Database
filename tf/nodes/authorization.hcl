# Inject the authorization module.

terraform {
  source = "../../../..//modules/infra/authorization/"
}

locals {
  env                = read_terragrunt_config(find_in_parent_folders("environment.hcl"))
  gha_oidc_role_name = local.env.locals.gha_oidc_role_name
  lock_table         = local.env.locals.lock_table
  oidc_allowed = [
    { org = "DALME", repo = "DALME-Online-Database", branch = "development.v2" },
  ]
}

inputs = {
  gha_oidc_role_name = local.gha_oidc_role_name
  lock_table         = local.lock_table
  oidc_allowed       = local.oidc_allowed
}
