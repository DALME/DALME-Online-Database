# IAM roles and permissions for the network module.

data "aws_iam_policy_document" "ssm_logs" {
  statement {
    effect = "Allow"
    actions = [
      "s3:GetEncryptionConfiguration",
    ]
    resources = [
      module.session_manager.logs_bucket_arn,
    ]

    principals {
      type        = "AWS"
      identifiers = var.allowed_roles
    }
  }

  statement {
    effect = "Allow"
    actions = [
      "s3:PutObject",
      "s3:PutObjectAcl",
    ]
    # tfsec:ignore:aws-iam-no-policy-wildcards
    resources = [
      module.session_manager.logs_bucket_arn,
      "${module.session_manager.logs_bucket_arn}/*",
    ]

    principals {
      type        = "AWS"
      identifiers = var.allowed_roles
    }
  }
}

resource "aws_s3_bucket_policy" "ssm_logs" {
  bucket = module.session_manager.logs_bucket_name
  policy = data.aws_iam_policy_document.ssm_logs.json
}

data "aws_iam_policy_document" "jump_host_policy_assume" {
  statement {
    actions = [
      "sts:AssumeRole",
    ]

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "jump_host_role" {
  name               = module.network_jh_role_label.id
  path               = "/"
  assume_role_policy = data.aws_iam_policy_document.jump_host_policy_assume.json

  tags = module.network_jh_role_label.tags
}

data "aws_iam_policy_document" "jump_host_policy_ssm" {
  statement {
    actions = [
      "kms:Decrypt",
    ]
    resources = [
      module.session_manager.kms_key_arn,
    ]
  }

  statement {
    actions = [
      "ec2messages:GetMessages",
    ]
    resources = [
      "arn:aws:ssm:*:${var.aws_account}:*",
    ]
  }

  statement {
    actions = [
      "s3:PutObject",
      "s3:PutObjectAcl",
      "s3:GetEncryptionConfiguration",
    ]
    # tfsec:ignore:aws-iam-no-policy-wildcards
    resources = [
      module.session_manager.logs_bucket_arn,
      "${module.session_manager.logs_bucket_arn}/*",
    ]
  }

  statement {
    actions = [
      "ssm:ListAssociations",
      "ssm:ListInstanceAssociations",
      "ssm:UpdateInstanceInformation",
      "ssmmessages:CreateControlChannel",
      "ssmmessages:CreateDataChannel",
      "ssmmessages:OpenControlChannel",
      "ssmmessages:OpenDataChannel",
    ]
    # tfsec:ignore:aws-iam-no-policy-wildcards
    resources = ["*"]
  }
}

resource "aws_iam_policy" "jump_host_policy_ssm" {
  name   = module.network_jh_policy_label.id
  policy = data.aws_iam_policy_document.jump_host_policy_ssm.json

  tags = module.network_jh_policy_label.tags
}

resource "aws_iam_role_policy_attachment" "jump_host_ssm" {
  policy_arn = aws_iam_policy.jump_host_policy_ssm.arn
  role       = aws_iam_role.jump_host_role.name
}

resource "aws_iam_instance_profile" "jump_host_profile" {
  role = aws_iam_role.jump_host_role.name
  path = "/"

  tags = module.network_jh_profile_label.tags
}
