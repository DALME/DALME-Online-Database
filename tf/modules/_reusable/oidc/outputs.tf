# Outputs for the oidc module.

output "gha_oidc_provider_arn" {
  description = "The ARN of the github OIDC provider resource."
  value       = aws_iam_openid_connect_provider.github.arn
}

output "gha_oidc_role_name" {
  description = "The name of the Github Actions OIDC role."
  value       = aws_iam_role.gha_oidc_role.name
}

output "label_id" {
  description = "The reusable id label for the oidc module."
  value       = module.oidc.id
}
