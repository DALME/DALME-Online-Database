# Terraform variables for the rds module.

variable "allocated_storage" {
  description = "The amount of storage for the db instance."
  type        = number
}

variable "backup_retention_period" {
  description = "How long to store db backups."
  type        = number
}

variable "db_name" {
  description = "The name of the db db instance."
  type        = string
}

variable "db_subnet_group_name" {
  description = "The subnet hosting the rds instance."
  type        = string
}

variable "deletion_protection" {
  description = "Whether or not deletion protection is activated for the db instance."
  type        = string
}

variable "engine" {
  description = "What type of database is the db instance."
  type        = string
}

variable "engine_version" {
  description = "The release version of the db instance."
  type        = number
}

variable "environment" {
  description = "Identify the deployment environment."
  type        = string
}

variable "iam_database_authentication_enabled" {
  description = "Allow db connections via IAM."
  type        = bool
}

variable "identifier" {
  description = "Names the rds resource itself."
  type        = string
}

variable "instance_class" {
  description = "The RDS db instance type."
  type        = string
}

variable "kms_key_arn" {
  description = "The project encryption key ARN."
  type        = string
}

variable "manage_master_user_password" {
  description = "Toggle automatic password opsec management."
  type        = bool
}

variable "multi_az" {
  description = "Is the db replicated across zones for failover."
  type        = bool
}

variable "parameter_rds_force_ssl" {
  description = "Require SSL to connect to the instance."
  type        = bool
}

variable "performance_insights_enabled" {
  description = "Specify whether Performance Insights are enabled."
  type        = bool
}

variable "performance_insights_retention_period" {
  description = "How long to preserve performance logs."
  type        = number
}

variable "port" {
  description = "The bound port of the db instance."
  type        = number
}

variable "publicly_accessible" {
  description = "Is db instance access exposed over the internet."
  type        = bool
}

variable "skip_final_snapshot" {
  description = "Whether to make a final db dump before deletion."
  type        = bool
}

variable "service" {
  description = "The service of the project/stack."
  type        = string
}

variable "storage_encrypted" {
  description = "Is the db instance data encrypted."
  type        = bool
}

variable "storage_type" {
  description = "Specify the storage media for the db instance."
  type        = string
}

variable "username" {
  description = "The user accessing the db."
  type        = string
}

variable "vpc_security_group_ids" {
  description = "Identify the RDS security group(s)."
  type        = list(string)
}
