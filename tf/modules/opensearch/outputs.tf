# Terraform outputs for the opensearch module.

output "endpoint" {
  description = "Domain-specific endpoint to submit OpenSearch requests."
  value       = aws_opensearch_domain.main.endpoint
}

output "master_user_name" {
  description = "Login user for the OpenSearch service."
  value       = local.master_user_name
}
