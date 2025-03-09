# Outputs for the ssm module.

output "kms_key_arn" {
  description = "ARN of the SSM KMS key"
  value       = aws_kms_key.ssm_key.arn
}

output "logs_bucket_arn" {
  description = "ARN of the SSM logs bucket."
  value       = module.ssm_logs.bucket_arn
}

output "logs_bucket_name" {
  description = "The name/id of the SSM logs bucket."
  value       = module.ssm_logs.bucket_id
}
