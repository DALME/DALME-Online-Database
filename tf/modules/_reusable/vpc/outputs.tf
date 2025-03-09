# Outputs for the vpc module.

output "vpc_id" {
  description = "Identifier for the VPC."
  value       = aws_vpc.this.id
}

output "subnets" {
  description = "Bundle VPC subnet identifiers."
  value = {
    private = aws_subnet.private[*].id
    public  = aws_subnet.public[*].id
  }
}
