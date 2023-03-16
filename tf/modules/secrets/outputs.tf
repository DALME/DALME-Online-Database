# Terraform outputs for the secrets module.

locals {
  index = zipmap(var.secrets, aws_secretsmanager_secret_version.secrets_values[*])
  secret_values = {
    for secret in var.secrets : secret => lookup(local.index, secret)
  }
  secrets_map = {
    for secret in var.secrets : secret => {
      name      = secret,
      valueFrom = lookup(local.index, secret).arn,
    }
  }
}

output "kms_key_arn" {
  description = "ARN for the project KMS encryption key."
  value       = aws_kms_key.main.arn
}

output "secrets_arns" {
  description = "AWS identifiers for the registered secrets."
  value       = aws_secretsmanager_secret_version.secrets_values[*].arn
}

output "secrets" {
  description = "A map of secrets from name to name/value 'Secret' objects."
  value       = local.secrets_map
}

output "opensearch_password" {
  description = "The opensearch master user password ARN."
  value       = lookup(local.secret_values, "OPENSEARCH_PASSWORD").secret_string
  sensitive   = true
}
