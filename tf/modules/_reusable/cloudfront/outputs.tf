# Outputs for the cloudfront module.

output "arn" {
  description = "ARN for the distribution."
  value       = aws_cloudfront_distribution.this.arn
}
