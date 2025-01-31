# Outputs for the rds module.

output "security_group_id" {
  description = "Identifier for the RDS instance's security group."
  value       = aws_security_group.this.id
}

output "security_group_label_context" {
  description = "Label data for the RDS instance's security group."
  value       = module.rds_sg_label.context
}
