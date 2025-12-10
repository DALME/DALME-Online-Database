# Outputs for the oidc module.

output "provider_arn" {
  description = "The ARN of the github OIDC provider resource."
  value       = aws_iam_openid_connect_provider.github.arn
}

output "role_arn" {
  description = "The ARN of the Github Actions OIDC role."
  value       = aws_iam_role.this.arn
}

output "role_name" {
  description = "The name of the Github Actions OIDC role."
  value       = aws_iam_role.this.name
}
