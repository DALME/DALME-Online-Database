terraform {
  source = "../../../modules//secrets/"

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
  env         = read_terragrunt_config(find_in_parent_folders("env.hcl"))
  region_env  = read_terragrunt_config(find_in_parent_folders("region.hcl"))
  account_ids = local.env.locals.account_ids
  aws_account = local.env.locals.aws_account
  aws_region  = local.region_env.locals.aws_region
  environment = local.env.locals.environment
  service     = local.env.locals.service
}

inputs = {
  account_ids     = local.account_ids
  aws_account     = local.aws_account
  aws_region      = local.aws_region
  environment     = local.environment
  keeper          = 1
  recovery_window = local.environment == "production" ? 7 : 0
  secrets         = ["ADMIN_PASSWORD", "OPENSEARCH_PASSWORD", "DJANGO_SECRET_KEY"]
  service         = local.service
  static_secrets  = ["ADMIN_PASSWORD"]
}
