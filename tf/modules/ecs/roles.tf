# IAM roles and permissions for the ecs module.

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
  # TODO: Why is this here?
  statement {
    effect = "Allow"
    actions = [
      "cloudfront:CreateInvalidation",
    ]
    resources = [var.cloudfront_arn]
  }

  statement {
    effect = "Allow"
    actions = [
      "kms:Decrypt",
    ]
    resources = [var.kms_key_arn]
  }

  statement {
    effect = "Allow"
    # tfsec:ignore:aws-iam-no-policy-wildcards
    actions = [
      "secretsmanager:GetSecretValue",
    ]
    resources = concat(
      var.secrets_arns,
      [var.postgres_password_secret_arn],
    )
  }

  statement {
    effect = "Allow"
    actions = [
      "s3:DeleteObject",
      "s3:GetObject",
      "s3:GetObjectAcl",
      "s3:ListBucket",
      "s3:PutObject",
      "s3:PutObjectAcl",
    ]
    resources = [
      var.staticfiles_arn,
      "${var.staticfiles_arn}/*",
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
    resources = var.repository_arns
  }

  statement {
    effect = "Allow"
    actions = [
      "kms:Decrypt",
    ]
    resources = [var.kms_key_arn]
  }

  statement {
    effect = "Allow"
    actions = [
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]
    # tfsec:ignore:aws-iam-no-policy-wildcards
    resources = [
      "${aws_cloudwatch_log_group.proxy_log_group.arn}:log-stream:*",
      "${aws_cloudwatch_log_group.web_log_group.arn}:log-stream:*",
    ]
  }

  statement {
    effect = "Allow"
    # tfsec:ignore:aws-iam-no-policy-wildcards
    actions = [
      "secretsmanager:GetSecretValue",
    ]
    resources = concat(
      var.secrets_arns,
      [var.postgres_password_secret_arn],
    )
  }
}

# https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_execution_IAM_role.html
resource "aws_iam_role" "ecs_task_execution_role" {
  name               = "${var.service}-ecs-task-execution-role-${var.environment}"
  assume_role_policy = data.aws_iam_policy_document.ecs_task_execution_role.json

  tags = {
    Name = "${var.service}-ecs-task-execution-role-${var.environment}"
  }
}

resource "aws_iam_policy" "ecs_task_execution_policy" {
  name   = "${var.service}-ecs-task-execution-policy-${var.environment}"
  policy = data.aws_iam_policy_document.ecs_task_execution_policy.json

  tags = {
    Name = "${var.service}-ecs-task-execution-policy-${var.environment}"
  }
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution_role" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = aws_iam_policy.ecs_task_execution_policy.arn
}

# https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-iam-roles.html
resource "aws_iam_role" "ecs_task_role" {
  name               = "${var.service}-ecs-task-role-${var.environment}"
  assume_role_policy = data.aws_iam_policy_document.ecs_task_role.json

  tags = {
    Name = "${var.service}-ecs-task-role-${var.environment}"
  }
}

resource "aws_iam_policy" "ecs_task_policy" {
  name   = "${var.service}-ecs-task-policy-${var.environment}"
  policy = data.aws_iam_policy_document.ecs_task_policy.json

  tags = {
    Name = "${var.service}-ecs-task-policy-${var.environment}"
  }
}

resource "aws_iam_role_policy_attachment" "ecs_task_role" {
  role       = aws_iam_role.ecs_task_role.name
  policy_arn = aws_iam_policy.ecs_task_policy.arn
}

// Cloudwatch events
data "aws_iam_policy_document" "cloudwatch_scheduled_task_role" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      identifiers = ["events.amazonaws.com"]
      type        = "Service"
    }
  }
}

data "aws_iam_policy_document" "cloudwatch_scheduled_task_policy" {
  statement {
    effect  = "Allow"
    actions = ["states:StartExecution"]
    resources = [
      aws_sfn_state_machine.publish.id,
    ]
  }
}

resource "aws_iam_role" "cloudwatch_scheduled_task_role" {
  name               = "${var.service}-cloudwatch-scheduled-task-role-${var.environment}"
  assume_role_policy = data.aws_iam_policy_document.cloudwatch_scheduled_task_role.json

  tags = {
    Name = "${var.service}-cloudwatch-scheduled-task-role-${var.environment}"
  }
}

resource "aws_iam_policy" "cloudwatch_scheduled_task_policy" {
  name   = "${var.service}-cloudwatch-scheduled-task-policy-${var.environment}"
  policy = data.aws_iam_policy_document.cloudwatch_scheduled_task_policy.json

  tags = {
    Name = "${var.service}-cloudwatch-scheduled-task-policy-${var.environment}"
  }
}

resource "aws_iam_role_policy_attachment" "cloudwatch_scheduled_task_role" {
  role       = aws_iam_role.cloudwatch_scheduled_task_role.name
  policy_arn = aws_iam_policy.cloudwatch_scheduled_task_policy.arn
}

// Step functions
data "aws_iam_policy_document" "sfn_role_policy" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["states.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "sfn_execution_policy" {
  statement {
    effect = "Allow"
    actions = [
      "events:PutTargets",
      "events:PutRule",
      "events:DescribeRule",
    ]
    resources = [
      "arn:aws:events:${var.aws_region}:${var.aws_account}:rule/StepFunctionsGetEventsForECSTaskRule",
    ]
  }

  statement {
    effect = "Allow"
    actions = [
      "iam:PassRole",
      "iam:GetRole",
    ]
    resources = [
      aws_iam_role.ecs_task_role.arn,
      aws_iam_role.ecs_task_execution_role.arn,
    ]
  }

  statement {
    effect  = "Allow"
    actions = ["ecs:RunTask"]
    resources = [
      "arn:aws:ecs:${var.aws_region}:${var.aws_account}:task-definition/*"
    ]
  }

  statement {
    effect = "Allow"
    actions = [
      "ecs:StopTask",
      "ecs:DescribeTasks",
    ]
    # tfsec:ignore:aws-iam-no-policy-wildcards
    resources = ["*"]

    condition {
      test     = "ArnEquals"
      variable = "ecs:cluster"
      values   = [aws_ecs_cluster.main.arn]
    }
  }

  statement {
    effect = "Allow"
    actions = [
      "kms:Decrypt",
      "kms:GenerateDataKey",
    ]
    resources = [var.kms_key_arn]
  }

  statement {
    effect    = "Allow"
    actions   = ["sns:Publish"]
    resources = [aws_sns_topic.ecs_scheduled_task_failure.arn]
  }
}

resource "aws_iam_role" "sfn_execution_role" {
  name               = "${var.service}-sfn-execution-role-${var.environment}"
  assume_role_policy = data.aws_iam_policy_document.sfn_role_policy.json

  tags = {
    Name = "${var.service}-sfn-execution-role-${var.environment}"
  }
}

resource "aws_iam_policy" "sfn_execution_policy" {
  name   = "${var.service}-sfn-execution-policy-${var.environment}"
  policy = data.aws_iam_policy_document.sfn_execution_policy.json

  tags = {
    Name = "${var.service}-sfn-execution-policy-${var.environment}"
  }
}

resource "aws_iam_role_policy_attachment" "sfn_execution" {
  role       = aws_iam_role.sfn_execution_role.name
  policy_arn = aws_iam_policy.sfn_execution_policy.arn
}
