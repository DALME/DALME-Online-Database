terraform {
  source = "../../../modules//cloudfront/"

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
  env            = read_terragrunt_config(find_in_parent_folders("env.hcl"))
  aws_account    = local.env.locals.aws_account
  environment    = local.env.locals.environment
  service        = local.env.locals.service
  tenant_domains = local.env.locals.tenant_domains
}

dependency "alb" {
  config_path                             = "../alb/"
  skip_outputs                            = tobool(get_env("TF_SKIP_OUTPUTS", "false"))
  mock_outputs_allowed_terraform_commands = ["destroy", "init", "plan", "validate"]
  mock_outputs_merge_strategy_with_state  = "shallow"
  mock_outputs = {
    dns = "some-loadbalancer-0000000000.us-east-2.alb.amazonaws.com",
  }
}

dependency "waf" {
  config_path                             = "../waf/"
  skip_outputs                            = tobool(get_env("TF_SKIP_OUTPUTS", "false"))
  mock_outputs_allowed_terraform_commands = ["destroy", "init", "plan", "validate"]
  mock_outputs_merge_strategy_with_state  = "shallow"
  mock_outputs = {
    waf_arn = "arn:aws:wafv2:us-east-1:000000000000:REGIONAL/webacl/name/1234a1a-a1b1-12a1-abcd-a123b123456",
  }
}

inputs = {
  alb_dns         = dependency.alb.outputs.dns
  allowed_methods = ["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
  aws_account     = local.aws_account
  dns_ttl         = 60
  environment     = local.environment
  force_destroy   = local.environment == "staging"
  service         = local.service
  tenant_domains  = local.tenant_domains
  web_acl_id      = dependency.waf.outputs.waf_arn
}
