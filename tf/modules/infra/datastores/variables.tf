# Variables for the datastores module.

variable "domain" {
  description = "The origin of the service."
  type        = string
}

variable "opensearch" {
  description = "Configuration for managing an instance of opensearch."
  type = object({
    admins                        = list(string)
    dedicated_master_count        = number
    dedicated_master_enabled      = bool
    dns_ttl                       = number
    ebs_enabled                   = bool
    ebs_throughput                = number
    ebs_volume_size               = number
    ebs_volume_type               = string
    encrypt_at_rest               = bool
    engine_version                = string
    instance_count                = number
    instance_type                 = string
    keepers                       = object({ master_user_version = number })
    log_retention_in_days         = number
    node_to_node_encryption       = bool
    opensearch_master_user_secret_name = string
    port                          = number
    recovery_window               = number
    security_options_enabled      = bool
    zone_awareness_enabled        = bool
  })
}

# This could be more dynamic (a list) if you have multiple RDS instances but
# it's not necessary for us at the moment so we'll just make it flat.
variable "rds_postgres" {
  description = "Configuration for an RDS instance."
  type = object({
    allocated_storage                     = number
    apply_immediately                     = bool
    backup_retention_period               = number
    cidr_blocks                           = string
    db_name                               = string
    deletion_protection                   = bool
    engine                                = string
    engine_version                        = number
    iam_database_authentication_enabled   = bool
    identifier                            = string
    instance_class                        = string
    ipv6_cidr_blocks                      = string
    manage_master_user_password           = bool
    multi_az                              = bool
    parameter_rds_force_ssl               = bool
    performance_insights_enabled          = bool
    performance_insights_retention_period = number
    port                                  = number
    publicly_accessible                   = bool
    skip_final_snapshot                   = bool
    storage_encrypted                     = bool
    storage_type                          = string
    username                              = string
  })
}
