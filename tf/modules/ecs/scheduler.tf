# Terraform definitions for the ecs publish tasks.
# https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/publishEvents.html#CronExpressions

resource "aws_sns_topic" "ecs_scheduled_task_failure" {
  name              = "${var.service}-sns-ecs-scheduled-task-failure-${var.environment}"
  kms_master_key_id = var.kms_key_arn
  delivery_policy = jsonencode({
    "http" : {
      "defaultHealthyRetryPolicy" : {
        "minDelayTarget" : 20,
        "maxDelayTarget" : 20,
        "numRetries" : 3,
        "numMaxDelayRetries" : 0,
        "numNoDelayRetries" : 0,
        "numMinDelayRetries" : 0,
        "backoffFunction" : "linear"
      },
      "disableSubscriptionOverrides" : false,
      "defaultThrottlePolicy" : {
        "maxReceivesPerSecond" : 1
      }
    }
  })

  tags = {
    Name = "${var.service}-sns-ecs-scheduled-task-failure-${var.environment}"
  }
}

resource "aws_sns_topic_subscription" "ecs_scheduled_task_failure" {
  count     = length(var.admins)
  topic_arn = aws_sns_topic.ecs_scheduled_task_failure.arn
  protocol  = "email"
  endpoint  = var.admins[count.index]
}

# Publish wagtail scheduled pages scheduled task.
resource "aws_ecs_task_definition" "publish" {
  family                   = "${var.service}-task-definition-publish-${var.environment}"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.fargate_cpu
  memory                   = var.fargate_memory
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_role.arn

  depends_on = [
    aws_ecs_task_definition.main
  ]

  container_definitions = jsonencode([
    {
      name        = "publish"
      image       = local.web_image
      environment = local.web_env
      secrets     = local.secrets
      essential   = true
      command = [
        "python3",
        "manage.py",
        "all_tenants_command",
        "publish_pages",
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.web_log_group.name
          awslogs-region        = var.aws_region
          awslogs-stream-prefix = "ecs-scheduled"
        }
      }
    },
  ])

  tags = {
    Name = "${var.service}-ecs-task-definition-publish-${var.environment}"
  }
}

locals {
  publish = var.scheduled_tasks.publish
}

resource "aws_cloudwatch_event_rule" "publish" {
  name                = "${var.service}-cloudwatch-event-rule-publish-${var.environment}"
  description         = "Publish Wagtail pages scheduled to go live."
  is_enabled          = local.publish.is_enabled
  schedule_expression = local.publish.schedule_expression

  tags = {
    Name = "${var.service}-cloudwatch-event-rule-publish-${var.environment}"
  }
}

resource "aws_cloudwatch_event_target" "publish" {
  arn       = aws_sfn_state_machine.publish.arn
  rule      = aws_cloudwatch_event_rule.publish.name
  role_arn  = aws_iam_role.cloudwatch_scheduled_task_role.arn
  target_id = "${var.service}-cloudwatch-event-target-publish-${var.environment}"
}

resource "aws_sfn_state_machine" "publish" {
  name     = "${var.service}-sfn-state-machine-publish-${var.environment}"
  role_arn = aws_iam_role.sfn_execution_role.arn

  definition = templatefile("${path.module}/files/scheduled-task.json.tmpl", {
    assign_public_ip       = local.publish.assign_public_ip == true ? "ENABLED" : "DISABLED"
    backoff_rate           = var.sfn_backoff_rate
    cluster                = aws_ecs_cluster.main.arn
    container              = "publish"
    failure_sns_topic      = aws_sns_topic.ecs_scheduled_task_failure.arn
    heartbeat              = var.sfn_heartbeat
    max_attempts           = var.sfn_max_attempts
    retry_interval         = var.sfn_retry_interval
    security_groups        = var.ecs_security_groups
    subnets                = var.subnets
    task_definition_family = replace(aws_ecs_task_definition.publish.arn, "/:\\d+$/", "")
    timeout                = var.sfn_timeout
  })

  tags = {
    Name = "${var.service}-sfn-state-machine-publish-${var.environment}"
  }
}

# Clear OAuth refresh tokens task.
# https://django-oauth-toolkit.readthedocs.io/en/latest/management_commands.html#createapplication
resource "aws_ecs_task_definition" "cleartokens" {
  family                   = "${var.service}-task-definition-cleartokens-${var.environment}"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.fargate_cpu
  memory                   = var.fargate_memory
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_role.arn

  depends_on = [
    aws_ecs_task_definition.main
  ]

  container_definitions = jsonencode([
    {
      name        = "cleartokens"
      image       = local.web_image
      environment = local.web_env
      secrets     = local.secrets
      essential   = true
      command = [
        "python3",
        "manage.py",
        "cleartokens",
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.web_log_group.name
          awslogs-region        = var.aws_region
          awslogs-stream-prefix = "ecs-scheduled"
        }
      }
    },
  ])

  tags = {
    Name = "${var.service}-ecs-task-definition-cleartokens-${var.environment}"
  }
}

locals {
  cleartokens = var.scheduled_tasks.cleartokens
}

resource "aws_cloudwatch_event_rule" "cleartokens" {
  name                = "${var.service}-cloudwatch-event-rule-cleartokens-${var.environment}"
  description         = "Remove expired OAuth refresh tokens."
  is_enabled          = local.cleartokens.is_enabled
  schedule_expression = local.cleartokens.schedule_expression

  tags = {
    Name = "${var.service}-cloudwatch-event-rule-cleartokens-${var.environment}"
  }
}

resource "aws_cloudwatch_event_target" "cleartokens" {
  arn       = aws_sfn_state_machine.cleartokens.arn
  rule      = aws_cloudwatch_event_rule.cleartokens.name
  role_arn  = aws_iam_role.cloudwatch_scheduled_task_role.arn
  target_id = "${var.service}-cloudwatch-event-target-cleartokens-${var.environment}"
}

resource "aws_sfn_state_machine" "cleartokens" {
  name     = "${var.service}-sfn-state-machine-cleartokens-${var.environment}"
  role_arn = aws_iam_role.sfn_execution_role.arn

  definition = templatefile("${path.module}/files/scheduled-task.json.tmpl", {
    assign_public_ip       = local.cleartokens.assign_public_ip == true ? "ENABLED" : "DISABLED"
    backoff_rate           = var.sfn_backoff_rate
    cluster                = aws_ecs_cluster.main.arn
    container              = "cleartokens"
    failure_sns_topic      = aws_sns_topic.ecs_scheduled_task_failure.arn
    heartbeat              = var.sfn_heartbeat
    max_attempts           = var.sfn_max_attempts
    retry_interval         = var.sfn_retry_interval
    security_groups        = var.ecs_security_groups
    subnets                = var.subnets
    task_definition_family = replace(aws_ecs_task_definition.cleartokens.arn, "/:\\d+$/", "")
    timeout                = var.sfn_timeout
  })

  tags = {
    Name = "${var.service}-sfn-state-machine-cleartokens-${var.environment}"
  }
}
