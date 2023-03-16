# Terraform outputs for the vpc module.

output "vpc_id" {
  description = "Identifier for the VPC."
  value       = aws_vpc.main.id
}

output "security_groups" {
  description = "Bundles security group identifiers."
  value = {
    alb        = aws_security_group.alb.id
    ecs        = aws_security_group.ecs.id
    opensearch = aws_security_group.opensearch.id
    postgres   = aws_security_group.postgres.id
  }
}

output "subnets" {
  description = "Bundles subnet identifiers."
  value = {
    postgres = aws_db_subnet_group.postgres.name
    private  = aws_subnet.private[*].id
    public   = aws_subnet.public[*].id
  }
}
