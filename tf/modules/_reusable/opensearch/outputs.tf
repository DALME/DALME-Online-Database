# Outputs for the opensearch module.

output "endpoint" {
  description = "Domain-specific endpoint to submit OpenSearch requests."
  value       = aws_opensearch_domain.this.endpoint
}

output "label_context" {
  description = "The root label context."
  value       = module.opensearch_label.context
}

output "security_group_id" {
  description = "Identify the security group controlling access to Opensearch."
  value       = aws_security_group.this.id
}
