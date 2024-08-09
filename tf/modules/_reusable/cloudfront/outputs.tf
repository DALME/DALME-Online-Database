# Outputs for the cloudfront module.

output "arn" {
  description = "ARN for the distribution."
  value       = aws_cloudfront_distribution.this.arn
}

output "domain_name" {
  description = "Domain name corresponding to the distribution."
  value       = aws_cloudfront_distribution.this.domain_name
}

output "hosted_zone_id" {
  description = "Route53 zone ID for the distribution."
  value       = aws_cloudfront_distribution.this.hosted_zone_id
}
