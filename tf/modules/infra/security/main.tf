# Entrypoint for the security module.

resource "aws_kms_key" "global" {
  description         = "Global KMS key per deploy environment."
  enable_key_rotation = true
  policy              = data.aws_iam_policy_document.kms.json

  tags = module.kms_label.tags
}

resource "aws_kms_alias" "global" {
  name          = "alias/${var.namespace}/global/${var.environment}"
  target_key_id = aws_kms_key.global.key_id
}
