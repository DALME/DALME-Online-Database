# Inject the datastores module.

terraform {
  source = "../../../..//modules/infra/datastores/"
}

locals {
  env         = read_terragrunt_config(find_in_parent_folders("environment.hcl"))
  environment = local.env.locals.environment
  namespace   = local.env.locals.namespace
  ports       = local.env.locals.ports
}

inputs = {
  # elasticsearch = {}
  rds_postgres = {
    allocated_storage                     = 20
    apply_immediately                     = contains(["development", "staging"], local.environment)
    backup_retention_period               = 7
    cidr_blocks                           = "0.0.0.0/0"
    db_name                               = local.namespace
    deletion_protection                   = local.environment == "production"
    engine                                = "postgres"
    engine_version                        = 15
    iam_database_authentication_enabled   = false
    instance_class                        = "db.t3.micro"
    ipv6_cidr_blocks                      = "::/0"
    storage_encrypted                     = true
    manage_master_user_password           = true
    multi_az                              = false
    parameter_rds_force_ssl               = false
    performance_insights_enabled          = true
    performance_insights_retention_period = 7
    port                                  = local.ports.postgres
    publicly_accessible                   = false
    skip_final_snapshot                   = contains(["development", "staging"], local.environment)
    storage_encrypted                     = true
    storage_type                          = "gp2"
    username                              = local.namespace
  }
}
