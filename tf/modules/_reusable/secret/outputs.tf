# Outputs for the secret module.

output "arn" {
  description = "ARN for the secret."
  value       = aws_secretsmanager_secret.this.arn
}

output "name" {
  description = "Name of the secret."
  value       = aws_secretsmanager_secret.this.name
}

output "version_arn" {
  description = "ARN for the secret version."
  value       = aws_secretsmanager_secret_version.this.arn
}
