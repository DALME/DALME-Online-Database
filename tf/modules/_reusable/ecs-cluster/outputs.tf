# Outputs for the ecs-cluster module.

output "arn" {
  description = "The ARN of the ECS cluster."
  value       = aws_ecs_cluster.this.arn
}

output "name" {
  description = "The name of the ecs cluster."
  value       = aws_ecs_cluster.this.name
}

output "security_group_id" {
  description = "Identify the security group controlling access to the ECS cluster."
  value       = aws_security_group.ecs.id
}
