terraform {
  source = "../../../modules//alb/"

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
  environment    = local.env.locals.environment
  ports          = local.env.locals.ports
  service        = local.env.locals.service
  tenant_domains = local.env.locals.tenant_domains
}

dependency "vpc" {
  config_path                             = "../vpc/"
  skip_outputs                            = tobool(get_env("TF_SKIP_OUTPUTS", "false"))
  mock_outputs_allowed_terraform_commands = ["destroy", "init", "plan", "validate"]
  mock_outputs_merge_strategy_with_state  = "shallow"
  mock_outputs = {
    security_groups = {
      alb = "sg-00000000000000000",
    },
    subnets = {
      public = ["subnet-0000000000000000"],
    },
    vpc_id = "vpc-00000000000000000",
  }
}

inputs = {
  alb_port                         = local.ports.alb
  dns_ttl                          = 60
  environment                      = local.environment
  health_check_interval            = 200
  health_check_matcher             = 200
  health_check_path                = "/api/healthcheck/"
  health_check_threshold           = 3
  health_check_timeout             = 10
  health_check_unhealthy_threshold = 3
  security_groups                  = [dependency.vpc.outputs.security_groups.alb]
  service                          = local.service
  ssl_port                         = local.ports.ssl
  subnets                          = dependency.vpc.outputs.subnets.public
  tenant_domains                   = local.tenant_domains
  vpc_id                           = dependency.vpc.outputs.vpc_id
}
