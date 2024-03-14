# Terraform outputs for the ecr module.

output "repository_arns" {
  description = "ARNs for repository containers."
  value       = aws_ecr_repository.images[*].arn
}
