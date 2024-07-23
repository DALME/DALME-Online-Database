# IAM roles and permissions for the security module.
#
data "aws_iam_policy_document" "kms" {
  # CAUTION: The existence of the following statement is critical.
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
      identifiers = var.allowed_roles
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
