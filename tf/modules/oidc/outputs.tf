# Terraform outputs for the oidc module.

output "gha_oidc_role_name" {
  description = "The name of the Github Actions OIDC role."
  value       = aws_iam_role.gha_oidc_role.name
}

output "oidc_provider_arn" {
  description = "ARN for the github OIDC connection/fingerprint."
  value       = aws_iam_openid_connect_provider.github.arn
}
