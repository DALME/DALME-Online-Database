# Inject the datastores module.

terraform {
  source = "../../../..//modules/infra/datastores/"
}

locals {
  env                                = read_terragrunt_config(find_in_parent_folders("environment.hcl"))
  namespace                          = local.env.locals.namespace
  admins                             = local.env.locals.admins
  domain                             = local.env.locals.domain
  environment                        = local.env.locals.environment
  opensearch_master_user_secret_name = local.env.locals.opensearch_master_user_secret_name
  opensearch_version                 = local.env.locals.opensearch_version
  ports                              = local.env.locals.ports
  postgres_version                   = local.env.locals.postgres_version
}

inputs = {
  domain = local.domain
  opensearch = {
    admins = local.admins
    # https://docs.aws.amazon.com/opensearch-service/latest/developerguide/managedomains-dedicatedmasternodes.html#dedicatedmasternodes-instance
    # If dedicated_master_enabled is true then the dedicated_master_count should be 3.
    dedicated_master_enabled           = false
    dedicated_master_count             = 0
    dedicated_master_type              = null
    dns_ttl                            = 60
    ebs_enabled                        = true
    ebs_throughput                     = 250
    ebs_volume_size                    = 45
    ebs_volume_type                    = "gp3"
    encrypt_at_rest                    = true
    engine_version                     = local.opensearch_version
    instance_count                     = 1
    instance_type                      = "t3.small.search"
    keepers                            = { master_user_version = 1 }
    log_retention_in_days              = 14
    node_to_node_encryption            = true
    opensearch_master_user_secret_name = local.opensearch_master_user_secret_name
    port                               = local.ports.opensearch
    recovery_window                    = local.environment == "production" ? 7 : 0
    security_options_enabled           = false # NOTE: This must be false for the initial provisioning.
    zone_awareness_enabled             = false
  }
  rds_postgres = {
    allocated_storage                     = 20
    apply_immediately                     = contains(["development", "staging"], local.environment)
    backup_retention_period               = 7
    cidr_blocks                           = "0.0.0.0/0"
    db_name                               = local.namespace
    deletion_protection                   = local.environment == "production"
    engine                                = "postgres"
    engine_version                        = local.postgres_version
    iam_database_authentication_enabled   = false
    identifier                            = "rds-postgres"
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
