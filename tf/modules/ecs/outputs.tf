# Terraform outputs for the ecs module.

output "ecs_cluster" {
  description = "The name of the ecs cluster."
  value       = aws_ecs_cluster.main.name
}

output "ecs_service" {
  description = "The name of the ecs service."
  value       = aws_ecs_service.main.name
}
