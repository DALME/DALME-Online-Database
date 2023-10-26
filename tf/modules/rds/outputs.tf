# Terraform outputs for the rds module.

output "address" {
  description = "The address of the RDS instance."
  value       = aws_db_instance.main.address
}

output "db_user" {
  description = "IAM user with permissions to access the database."
  value       = aws_iam_user.db_user.name
  sensitive   = true
}

output "master_user_secret_arn" {
  description = "The ARN of the db instance password secret."
  value       = aws_db_instance.main.master_user_secret[0].secret_arn
}

output "name" {
  description = "The name of the RDS instance."
  value       = aws_db_instance.main.db_name
}

output "username" {
  description = "The main username of the RDS instance."
  value       = aws_db_instance.main.username
}

output "rds_instance_arn" {
  description = "The ARN of the RDS instance."
  value       = aws_db_instance.main.arn
}
