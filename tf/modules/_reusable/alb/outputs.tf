# Outputs for the alb module.

output "security_group_id" {
  description = "Identify the security group controlling access to the ALB."
  value       = aws_security_group.alb.id
}
