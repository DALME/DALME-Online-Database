# Entrypoint for the rds module.
locals {
  apply_method = contains(["development", "staging"], var.environment) ? "immediate" : "pending-reboot"
  family       = "${var.engine}${var.engine_version}"
}

resource "aws_db_parameter_group" "this" {
  family = local.family
  name   = module.rds_pg_label.id

  lifecycle {
    create_before_destroy = true
  }

  parameter {
    # Enforce SSL connections.
    name         = "rds.force_ssl"
    value        = var.parameter_rds_force_ssl
    apply_method = local.apply_method
  }

  tags = module.rds_pg_label.tags
}

resource "aws_db_subnet_group" "this" {
  name       = module.rds_sbng_label.id
  subnet_ids = var.subnet_ids

  tags = module.rds_sbng_label.tags
}

resource "aws_security_group" "this" {
  description = "Security group for the RDS instance."
  name_prefix = module.rds_sg_label.id
  vpc_id      = var.vpc_id

  lifecycle {
    create_before_destroy = true
  }

  tags = module.rds_sg_label.tags
}

resource "aws_db_instance" "this" {
  allocated_storage                     = var.allocated_storage
  apply_immediately                     = var.apply_immediately
  backup_retention_period               = var.backup_retention_period
  db_name                               = var.db_name
  db_subnet_group_name                  = aws_db_subnet_group.this.name
  deletion_protection                   = var.deletion_protection # tfsec:ignore:AVD-AWS-0177
  engine                                = var.engine
  engine_version                        = var.engine_version
  iam_database_authentication_enabled   = var.iam_database_authentication_enabled
  identifier                            = module.rds_label.id
  instance_class                        = var.instance_class
  kms_key_id                            = var.kms_key_arn
  manage_master_user_password           = var.manage_master_user_password
  master_user_secret_kms_key_id         = var.kms_key_arn
  multi_az                              = var.multi_az
  parameter_group_name                  = aws_db_parameter_group.this.name
  performance_insights_enabled          = var.performance_insights_enabled
  performance_insights_kms_key_id       = var.kms_key_arn
  performance_insights_retention_period = var.performance_insights_retention_period
  port                                  = var.port
  publicly_accessible                   = var.publicly_accessible
  skip_final_snapshot                   = var.skip_final_snapshot
  storage_encrypted                     = var.storage_encrypted
  storage_type                          = var.storage_type
  username                              = var.username
  vpc_security_group_ids                = [aws_security_group.this.id]

  tags = module.rds_label.tags
}
