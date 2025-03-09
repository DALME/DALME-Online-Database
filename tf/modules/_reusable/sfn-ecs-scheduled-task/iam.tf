# IAM roles and permissions for the sfn-ecs-scheduled-task module.

# Cloudwatch events.
data "aws_iam_policy_document" "cloudwatch_event_role" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      identifiers = ["events.amazonaws.com"]
      type        = "Service"
    }
  }
}

data "aws_iam_policy_document" "cloudwatch_event_policy" {
  statement {
    effect  = "Allow"
    actions = ["states:StartExecution"]
    resources = [
      aws_sfn_state_machine.this.id,
    ]
  }
}

resource "aws_iam_role" "cloudwatch_event_role" {
  name               = module.sfn_ecs_scheduled_task_event_role_label.id
  assume_role_policy = data.aws_iam_policy_document.cloudwatch_event_role.json

  tags = module.sfn_ecs_scheduled_task_event_role_label.tags
}

resource "aws_iam_policy" "cloudwatch_event_policy" {
  name   = module.sfn_ecs_scheduled_task_event_policy_label.id
  policy = data.aws_iam_policy_document.cloudwatch_event_policy.json

  tags = module.sfn_ecs_scheduled_task_event_policy_label.tags
}

resource "aws_iam_role_policy_attachment" "cloudwatch_event_role" {
  role       = aws_iam_role.cloudwatch_event_role.name
  policy_arn = aws_iam_policy.cloudwatch_event_policy.arn
}

# Step functions.
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
      var.ecs_task_role_arn,
      var.ecs_task_execution_role_arn,
    ]
  }

  statement {
    effect    = "Allow"
    actions   = ["ecs:RunTask"]
    resources = ["${local.task_definition_family}:*"]
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
      values   = [var.cluster]
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
    resources = [var.failure_sns_topic]
  }
}

resource "aws_iam_role" "sfn_execution_role" {
  name               = module.sfn_ecs_scheduled_task_execution_role_label.id
  assume_role_policy = data.aws_iam_policy_document.sfn_role_policy.json

  tags = module.sfn_ecs_scheduled_task_execution_role_label.tags
}

resource "aws_iam_policy" "sfn_execution_policy" {
  name   = module.sfn_ecs_scheduled_task_execution_policy_label.id
  policy = data.aws_iam_policy_document.sfn_execution_policy.json

  tags = module.sfn_ecs_scheduled_task_execution_policy_label.tags
}

resource "aws_iam_role_policy_attachment" "sfn_execution" {
  role       = aws_iam_role.sfn_execution_role.name
  policy_arn = aws_iam_policy.sfn_execution_policy.arn
}
