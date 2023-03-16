terraform {
  source = "../../../modules//opensearch/"

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
  admins         = local.env.locals.admins
  aws_account    = local.env.locals.aws_account
  aws_region     = local.region_env.locals.aws_region
  environment    = local.env.locals.environment
  service        = local.env.locals.service
  tenant_domains = local.env.locals.tenant_domains
}

dependency "secrets" {
  config_path                             = "../secrets/"
  skip_outputs                            = tobool(get_env("TF_SKIP_OUTPUTS", "false"))
  mock_outputs_allowed_terraform_commands = ["destroy", "init", "plan", "validate"]
  mock_outputs_merge_strategy_with_state  = "shallow"
  mock_outputs = {
    kms_key_arn         = "arn:aws:kms:us-east-1:000000000000:key/00000000-0000-0000-0000-000000000000",
    opensearch_password = "some-secret-password"
  }
}

dependency "vpc" {
  config_path                             = "../vpc/"
  skip_outputs                            = tobool(get_env("TF_SKIP_OUTPUTS", "false"))
  mock_outputs_allowed_terraform_commands = ["destroy", "init", "plan", "validate"]
  mock_outputs_merge_strategy_with_state  = "shallow"
  mock_outputs = {
    security_groups = {
      opensearch = "sg-00000000000000000",
    },
    subnets = {
      private = [
        "subnet-00000000000000000",
        "subnet-00000000000000001"
      ],
    },
    vpc_id = "vpc-00000000000000000",
  }
}

inputs = {
  admins                 = local.admins
  aws_account            = local.aws_account
  aws_region             = local.aws_region
  dedicated_master_count = 0
  # https://docs.aws.amazon.com/opensearch-service/latest/developerguide/managedomains-dedicatedmasternodes.html#dedicatedmasternodes-instance
  # If dedicated_master_enabled is true then the dedicated_master_count should be 3.
  dedicated_master_enabled = false
  dedicated_master_type    = null
  dns_ttl                  = 60
  ebs_enabled              = true
  ebs_throughput           = 250
  ebs_volume_size          = 45
  ebs_volume_type          = "gp3"
  encrypt_at_rest          = true
  engine_version           = "Elasticsearch_7.7"
  environment              = local.environment
  instance_count           = 1
  instance_type            = "t3.small.search"
  kms_key_arn              = dependency.secrets.outputs.kms_key_arn
  log_retention_in_days    = 14
  master_user_password     = dependency.secrets.outputs.opensearch_password
  node_to_node_encryption  = true
  security_group_ids       = [dependency.vpc.outputs.security_groups.opensearch]
  security_options_enabled = false # NOTE: This must be false for the initial provisioning.
  service                  = local.service
  subnet_ids               = dependency.vpc.outputs.subnets.private
  tenant_domains           = local.tenant_domains
  zone_awareness_enabled   = false
}
