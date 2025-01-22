# IAM roles and permissions for the ida module.

locals {
  secret_arns = [
    data.aws_secretsmanager_secret_version.dam.arn,
    data.aws_secretsmanager_secret_version.oidc_rsa_key.arn,
    data.aws_secretsmanager_secret_version.opensearch_master_user.arn,
    data.aws_secretsmanager_secret_version.zotero.arn,
    local.postgres_master_user_secret_arn,
    module.secret["ADMIN-USER"].arn,
    module.secret["DJANGO-SECRET-KEY"].arn,
    module.secret["OAUTH-CLIENT-SECRET"].arn,
  ]
}

# ECS task
data "aws_iam_policy_document" "ecs_task_role" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      identifiers = ["ecs-tasks.amazonaws.com"]
      type        = "Service"
    }

    # https://docs.aws.amazon.com/IAM/latest/UserGuide/confused-deputy.html
    condition {
      test     = "ArnLike"
      variable = "aws:SourceArn"
      values   = ["arn:aws:ecs:${var.aws_region}:${var.aws_account}:*"]
    }

    condition {
      test     = "StringEquals"
      variable = "aws:SourceAccount"
      values   = [var.aws_account]
    }
  }
}

data "aws_iam_policy_document" "ecs_task_policy" {
  statement {
    effect = "Allow"
    actions = [
      "cloudfront:CreateInvalidation",
    ]
    resources = [data.external.cloudfront.result.arn]
  }

  statement {
    effect = "Allow"
    actions = [
      "kms:Decrypt",
    ]
    resources = [data.aws_kms_alias.global.target_key_arn]
  }

  statement {
    effect = "Allow"
    # tfsec:ignore:aws-iam-no-policy-wildcards
    actions = [
      "secretsmanager:GetSecretValue",
    ]
    resources = local.secret_arns
  }

  statement {
    effect = "Allow"
    actions = [
      "s3:DeleteObject",
      "s3:GetObject",
      "s3:ListBucket",
      "s3:PutObject",
    ]
    # tfsec:ignore:aws-iam-no-policy-wildcards
    resources = [
      data.aws_s3_bucket.staticfiles.arn,
      "${data.aws_s3_bucket.staticfiles.arn}/*",
    ]
  }

  statement {
    effect = "Allow"
    actions = [
      "states:SendTaskSuccess",
    ]
    resources = [
      "arn:aws:states:${var.aws_region}:${var.aws_account}:stateMachine:*",
    ]
  }

}

# ECS task execution
data "aws_iam_policy_document" "ecs_task_execution_role" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      identifiers = ["ecs-tasks.amazonaws.com"]
      type        = "Service"
    }
  }
}

data "aws_iam_policy_document" "ecs_task_execution_policy" {
  statement {
    effect = "Allow"
    actions = [
      "ecr:GetAuthorizationToken",
    ]
    resources = ["*"] # NOTE: Can't be finer-grained in this case.
  }

  statement {
    effect = "Allow"
    actions = [
      "ecr:BatchCheckLayerAvailability",
      "ecr:GetDownloadUrlForLayer",
      "ecr:BatchGetImage",
    ]
    resources = [
      "arn:aws:ecr:${var.aws_region}:${var.aws_account}:repository/${var.namespace}.proxy",
      "arn:aws:ecr:${var.aws_region}:${var.aws_account}:repository/${var.namespace}.app",
    ]
  }

  statement {
    effect = "Allow"
    actions = [
      "kms:Decrypt",
    ]
    resources = [data.aws_kms_alias.global.target_key_arn]
  }

  statement {
    effect = "Allow"
    actions = [
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]
    # tfsec:ignore:aws-iam-no-policy-wildcards
    resources = [
      "${aws_cloudwatch_log_group.web_log_group.arn}:log-stream:*",
      "${aws_cloudwatch_log_group.proxy_log_group.arn}:log-stream:*",
    ]
  }

  statement {
    effect = "Allow"
    # tfsec:ignore:aws-iam-no-policy-wildcards
    actions = [
      "secretsmanager:GetSecretValue",
    ]
    resources = local.secret_arns
  }
}

# https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_execution_IAM_role.html
resource "aws_iam_role" "ecs_task_execution_role" {
  name               = module.ida_ecs_task_execution_role_label.id
  assume_role_policy = data.aws_iam_policy_document.ecs_task_execution_role.json

  tags = module.ida_ecs_task_execution_role_label.tags
}

resource "aws_iam_policy" "ecs_task_execution_policy" {
  name   = module.ida_ecs_task_execution_policy_label.id
  policy = data.aws_iam_policy_document.ecs_task_execution_policy.json

  tags = module.ida_ecs_task_execution_policy_label.tags
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution_role" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = aws_iam_policy.ecs_task_execution_policy.arn
}

# https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-iam-roles.html
resource "aws_iam_role" "ecs_task_role" {
  name               = module.ida_ecs_task_role_label.id
  assume_role_policy = data.aws_iam_policy_document.ecs_task_role.json

  tags = module.ida_ecs_task_role_label.tags
}

resource "aws_iam_policy" "ecs_task_policy" {
  name   = module.ida_ecs_task_policy_label.id
  policy = data.aws_iam_policy_document.ecs_task_policy.json

  tags = module.ida_ecs_task_policy_label.tags
}

resource "aws_iam_role_policy_attachment" "ecs_task_role" {
  role       = aws_iam_role.ecs_task_role.name
  policy_arn = aws_iam_policy.ecs_task_policy.arn
}
