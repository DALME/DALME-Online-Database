# Variables for the datastores module.

# variable "opensearch" {
#   description = "Configuration for managing an instance of elasticsearch."
#   type        = object({})
# }

# This could be more dynamic (a list) if you have multiple RDS instances but
# it's not necessary for us at the moment so we'll just make it flat.
variable "rds_postgres" {
  description = "Configuration for a PostgreSQL RDS instance."
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
