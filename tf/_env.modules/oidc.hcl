terraform {
  source = "../../../modules//oidc/"

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

locals {
  env                = read_terragrunt_config(find_in_parent_folders("env.hcl"))
  region_env         = read_terragrunt_config(find_in_parent_folders("region.hcl"))
  aws_account        = local.env.locals.aws_account
  aws_region         = local.region_env.locals.aws_region
  environment        = local.env.locals.environment
  gha_oidc_role_name = local.env.locals.gha_oidc_role_name
  lock_table         = local.env.locals.lock_table
  service            = local.env.locals.service
}

inputs = {
  aws_account        = local.aws_account
  aws_region         = local.aws_region
  environment        = local.environment
  gha_oidc_role_name = local.gha_oidc_role_name
  lock_table         = local.lock_table
  oidc_allowed = [
    { org = "ocp", repo = "DALME-Online-Database", branch = "ocp/development.v2" },
  ]
  service = local.service
}
