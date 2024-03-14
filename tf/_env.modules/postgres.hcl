terraform {
  source = "../../../modules//rds/"

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
  environment = local.env.locals.environment
  ports       = local.env.locals.ports
  service     = local.env.locals.service
}

dependency "secrets" {
  config_path                             = "../secrets/"
  skip_outputs                            = tobool(get_env("TF_SKIP_OUTPUTS", "false"))
  mock_outputs_allowed_terraform_commands = ["destroy", "init", "plan", "validate"]
  mock_outputs_merge_strategy_with_state  = "shallow"
  mock_outputs = {
    kms_key_arn = "arn:aws:kms:us-east-1:000000000000:key/00000000-0000-0000-0000-000000000000",
  }
}

dependency "vpc" {
  config_path                             = "../vpc/"
  skip_outputs                            = tobool(get_env("TF_SKIP_OUTPUTS", "false"))
  mock_outputs_allowed_terraform_commands = ["destroy", "init", "plan", "validate"]
  mock_outputs_merge_strategy_with_state  = "shallow"
  mock_outputs = {
    security_groups = {
      postgres = "sg-00000000000000000",
    },
    subnets = {
      postgres = "subnet-00000000000000000",
    },
  }
}

inputs = {
  allocated_storage                     = 20
  backup_retention_period               = 7
  db_name                               = local.service
  db_subnet_group_name                  = dependency.vpc.outputs.subnets.postgres
  deletion_protection                   = local.environment == "production"
  engine                                = "postgres"
  engine_version                        = 15
  environment                           = local.environment
  iam_database_authentication_enabled   = false
  identifier                            = "${local.service}-rds-postgres-${local.environment}"
  instance_class                        = "db.t3.micro"
  kms_key_arn                           = dependency.secrets.outputs.kms_key_arn
  manage_master_user_password           = true
  multi_az                              = false
  parameter_rds_force_ssl               = false
  performance_insights_enabled          = true
  performance_insights_retention_period = 7
  port                                  = local.ports.postgres
  publicly_accessible                   = false
  vpc_security_group_ids                = [dependency.vpc.outputs.security_groups.postgres]
  service                               = local.service
  skip_final_snapshot                   = local.environment == "staging"
  storage_encrypted                     = false
  storage_type                          = "gp2"
  username                              = local.service
}
