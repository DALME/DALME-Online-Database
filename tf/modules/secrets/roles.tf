# IAM roles and permissions for the secrets module.

### -- KMS default policy
data "aws_iam_policy_document" "kms" {
  # https://docs.aws.amazon.com/kms/latest/developerguide/key-policy-default.html#key-policy-default-allow-root-enable-iam
  statement {
    effect = "Allow"

    principals {
      identifiers = [
        "arn:aws:iam::${var.aws_account}:root"
      ]
      type = "AWS"
    }

    # tfsec:ignore:aws-iam-no-policy-wildcards
    actions   = ["kms:*"]
    resources = ["*"]
  }

  statement {
    effect = "Allow"

    principals {
      identifiers = var.account_ids
      type        = "AWS"
    }

    # tfsec:ignore:aws-iam-no-policy-wildcards
    actions = [
      "kms:Create*",
      "kms:Describe*",
      "kms:Enable*",
      "kms:List*",
      "kms:Put*",
      "kms:Update*",
      "kms:Revoke*",
      "kms:Disable*",
      "kms:Get*",
      "kms:Delete*",
      "kms:TagResource",
      "kms:UntagResource",
      "kms:ScheduleKeyDeletion",
      "kms:CancelKeyDeletion",
    ]
    resources = ["*"]
  }

  statement {
    effect = "Allow"

    principals {
      identifiers = ["logs.${var.aws_region}.amazonaws.com"]
      type        = "Service"
    }

    # tfsec:ignore:aws-iam-no-policy-wildcards
    actions = [
      "kms:Decrypt*",
      "kms:Describe*",
      "kms:Encrypt*",
      "kms:GenerateDataKey*",
      "kms:ReEncrypt*",
    ]
    resources = [
      "arn:aws:kms:${var.aws_region}:${var.aws_account}:key/*",
    ]

    condition {
      test     = "ArnLike"
      variable = "kms:EncryptionContext:aws:logs:arn"
      values = [
        "arn:aws:logs:${var.aws_region}:${var.aws_account}:log-group:*"
      ]
    }
  }
}
