# Entrypoint for the ssm module.

# Use an independent KMS key to airlock SSM.
resource "aws_kms_key" "ssm_key" {
  description             = "Encrypts SSM user sessions."
  deletion_window_in_days = 10
  enable_key_rotation     = true

  tags = module.ssm_kms_label.tags
}

module "ssm_logs" {
  source = "..//bucket/"

  acl                      = "log-delivery-write"
  aws_account              = var.aws_account
  control_object_ownership = true
  environment              = var.environment
  force_destroy            = var.force_destroy
  name                     = "ssm-logs"
  namespace                = var.namespace
  object_ownership         = "ObjectWriter"

  lifecycle_rule = [
    {
      id     = "ssm"
      status = "Enabled"

      filter = {
        prefix = "/"
      }

      expiration = {
        days = 90
      }

      noncurrent_version_expiration = {
        noncurrent_days = 90
      }

      noncurrent_version_transition = {
        noncurrent_days = 30
        storage_class   = "STANDARD_IA"
      }
    }
  ]

  server_side_encryption_configuration = {
    rule = {
      apply_server_side_encryption_by_default = {
        sse_algorithm = "AES256"
      }
      bucket_key_enabled = true
    }
  }

  versioning = {
    enabled = true
  }
}

resource "aws_ssm_document" "session_manager" {
  name            = "SSM-SessionManagerRunShell"
  document_type   = "Session"
  document_format = "JSON"

  content = templatefile("${path.module}/files/ssm-session.json.tmpl", {
    aws_account = var.aws_account
    key_id      = aws_kms_key.ssm_key.id
    logs_bucket = module.ssm_logs.bucket_id
  })

  tags = module.ssm_label.tags
}
