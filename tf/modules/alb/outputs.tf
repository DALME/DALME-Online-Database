# Terraform outputs for the alb module.

output "dns" {
  description = "Load balancer DNS endpoint."
  value       = aws_lb.main.dns_name
}

output "target_group_arn" {
  description = "The target group for the ALB."
  value       = aws_lb_target_group.main.arn
}
