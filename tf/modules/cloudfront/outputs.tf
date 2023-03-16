# Terraform outputs for the cloudfront module.

output "arn" {
  description = "ARN for the distribution."
  value       = aws_cloudfront_distribution.main.arn
}

output "assets_arn" {
  description = "The ARN of the s3 bucket containing frontend assets."
  value       = module.assets.s3_bucket_arn
}

output "domain" {
  description = "Where the destribution is served."
  value       = aws_cloudfront_distribution.main.domain_name
}

output "staticfiles_arn" {
  description = "The ARN of the s3 bucket containing static and media files."
  value       = module.staticfiles.s3_bucket_arn
}

output "staticfiles_bucket" {
  description = "The name of the s3 bucket containing static and media files."
  value       = module.staticfiles.s3_bucket_id
}

output "staticfiles_domain" {
  description = "The s3 bucket's regionally qualified endpoint."
  value       = module.staticfiles.s3_bucket_bucket_regional_domain_name
}
