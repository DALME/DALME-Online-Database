# Terraform definitions for the rds module.

terraform {
  required_version = "~> 1.3"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.14.0"
    }
  }
}

resource "aws_db_instance" "main" {
  allocated_storage                     = var.allocated_storage
  apply_immediately                     = var.environment == "staging"
  backup_retention_period               = var.backup_retention_period
  db_name                               = var.db_name
  db_subnet_group_name                  = var.db_subnet_group_name
  deletion_protection                   = var.deletion_protection # tfsec:ignore:AVD-AWS-0177
  engine                                = var.engine
  engine_version                        = var.engine_version
  identifier                            = var.identifier
  instance_class                        = var.instance_class
  manage_master_user_password           = var.manage_master_user_password
  master_user_secret_kms_key_id         = var.kms_key_arn
  multi_az                              = var.multi_az
  parameter_group_name                  = aws_db_parameter_group.main.name
  performance_insights_enabled          = var.performance_insights_enabled
  performance_insights_kms_key_id       = var.kms_key_arn
  performance_insights_retention_period = var.performance_insights_retention_period
  port                                  = var.port
  publicly_accessible                   = var.publicly_accessible
  skip_final_snapshot                   = var.skip_final_snapshot
  storage_encrypted                     = var.storage_encrypted
  storage_type                          = var.storage_type
  username                              = var.username
  vpc_security_group_ids                = var.vpc_security_group_ids

  tags = {
    Name = var.identifier
  }
}

locals {
  family = "${var.engine}${var.engine_version}"
  name   = "${var.service}-rds-parameter-group-${var.environment}"
}

resource "aws_db_parameter_group" "main" {
  family = local.family
  name   = local.name

  lifecycle {
    create_before_destroy = true
  }

  parameter {
    # Enforce SSL connections.
    name         = "rds.force_ssl"
    value        = var.parameter_rds_force_ssl
    apply_method = var.environment == "staging" ? "immediate" : "pending-reboot"
  }

  tags = {
    Name = local.name
  }
}
