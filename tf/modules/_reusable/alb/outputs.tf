# Outputs for the alb module.

output "security_group_id" {
  description = "Identify the security group controlling access to the ALB."
  value       = aws_security_group.alb.id
}

output "security_group_label_context" {
  description = "Label data for the ALB security group."
  value       = module.alb_sg_label.context
}
