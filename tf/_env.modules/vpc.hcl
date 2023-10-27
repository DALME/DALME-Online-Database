terraform {
  source = "../../../modules//vpc/"

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
  region_env     = read_terragrunt_config(find_in_parent_folders("region.hcl"))
  account_ids    = local.env.locals.account_ids
  aws_account    = local.env.locals.aws_account
  aws_region     = local.region_env.locals.aws_region
  environment    = local.env.locals.environment
  ports          = local.env.locals.ports
  service        = local.env.locals.service
  tenant_domains = local.env.locals.tenant_domains
}

inputs = {
  account_ids            = local.account_ids
  aws_account            = local.aws_account
  az_count               = 2
  cidr                   = "10.0.0.0/16"
  destination_cidr_block = "0.0.0.0/0"
  environment            = local.environment
  force_destroy          = local.environment == "staging"
  service                = local.service
  security_groups = {
    cidr_blocks      = "0.0.0.0/0",
    ipv6_cidr_blocks = "::/0",
    protocol         = "tcp",
    opensearch_port  = local.ports.opensearch,
    postgres_port    = local.ports.postgres,
    proxy_port       = local.ports.proxy,
    ssl_port         = local.ports.ssl,
  }
}
