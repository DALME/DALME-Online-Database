# Entrypoint for the datastores module.

module "postgres" {
  source = "../..//_reusable/rds/"

  allocated_storage                     = var.rds_postgres.allocated_storage
  apply_immediately                     = var.rds_postgres.apply_immediately
  backup_retention_period               = var.rds_postgres.backup_retention_period
  db_name                               = var.rds_postgres.db_name
  deletion_protection                   = var.rds_postgres.deletion_protection
  engine                                = var.rds_postgres.engine
  engine_version                        = var.rds_postgres.engine_version
  environment                           = var.environment
  iam_database_authentication_enabled   = var.rds_postgres.iam_database_authentication_enabled
  identifier                            = var.rds_postgres.identifier
  instance_class                        = var.rds_postgres.instance_class
  kms_key_arn                           = var.rds_postgres.storage_encrypted ? data.aws_kms_alias.global.target_key_arn : null
  manage_master_user_password           = var.rds_postgres.manage_master_user_password
  multi_az                              = var.rds_postgres.multi_az
  namespace                             = var.namespace
  parameter_rds_force_ssl               = var.rds_postgres.parameter_rds_force_ssl
  performance_insights_enabled          = var.rds_postgres.performance_insights_enabled
  performance_insights_retention_period = var.rds_postgres.performance_insights_retention_period
  port                                  = var.rds_postgres.port
  publicly_accessible                   = var.rds_postgres.publicly_accessible
  skip_final_snapshot                   = var.rds_postgres.skip_final_snapshot
  storage_encrypted                     = var.rds_postgres.storage_encrypted
  storage_type                          = var.rds_postgres.storage_type
  subnet_ids                            = data.aws_subnets.private.ids
  username                              = var.rds_postgres.username
  vpc_id                                = data.aws_vpc.this.id
}

resource "aws_security_group_rule" "postgres_ingress_jump_host" {
  description              = "Allow incoming traffic to postgres from the jump host."
  security_group_id        = module.postgres.security_group_id
  type                     = "ingress"
  protocol                 = "tcp"
  from_port                = var.rds_postgres.port
  to_port                  = var.rds_postgres.port
  source_security_group_id = data.aws_security_group.tunnel.id
}

resource "aws_security_group_rule" "jump_host_egress_postgres" {
  description              = "Allow outgoing traffic to postgres from the jump host."
  security_group_id        = data.aws_security_group.tunnel.id
  type                     = "egress"
  protocol                 = "tcp"
  from_port                = var.rds_postgres.port
  to_port                  = var.rds_postgres.port
  source_security_group_id = module.postgres.security_group_id
}
