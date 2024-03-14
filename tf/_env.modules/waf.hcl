terraform {
  source = "../../../modules//waf/"

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
  aws_account = local.env.locals.aws_account
  environment = local.env.locals.environment
  service     = local.env.locals.service
}

inputs = {
  aws_account   = local.aws_account
  country       = "GB"
  environment   = local.environment
  force_destroy = true
  name          = "waf-cloudfront"
  service       = local.service
}
