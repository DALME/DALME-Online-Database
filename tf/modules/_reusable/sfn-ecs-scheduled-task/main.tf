# Entrypoint for the sfn-ecs-scheduled-task module.

# https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/publishEvents.html#CronExpressions
resource "aws_sns_topic" "ecs_scheduled_task_failure" {
  name              = module.sfn_ecs_scheduled_task_sns_topic_label.id
  kms_master_key_id = data.aws_kms_alias.global.target_key_arn
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

  tags = module.sfn_ecs_scheduled_task_sns_topic_label.tags
}

# TODO: We might want to consider parameterizing this...
resource "aws_sns_topic_subscription" "ecs_scheduled_task_failure" {
  count     = length(var.admins)
  topic_arn = aws_sns_topic.ecs_scheduled_task_failure.arn
  protocol  = "email"
  endpoint  = var.admins[count.index]
}

resource "aws_cloudwatch_event_rule" "this" {
  name                = module.sfn_ecs_scheduled_task_event_rule_label.id
  description         = var.description
  schedule_expression = var.schedule_expression
  state               = var.state

  tags = module.sfn_ecs_scheduled_task_event_rule_label.tags
}

resource "aws_sfn_state_machine" "this" {
  name = module.sfn_ecs_scheduled_task_label.id
  # TODO: Pass this in or do it here? Hrmmmm
  role_arn = aws_iam_role.sfn_execution_role.arn

  definition = templatefile("${path.module}/files/scheduled-task.json.tmpl", {
    assign_public_ip       = var.assign_public_ip == true ? "ENABLED" : "DISABLED"
    backoff_rate           = var.sfn_backoff_rate
    cluster                = data.aws_ecs_cluster.this.arn
    container              = var.container
    failure_sns_topic      = aws_sns_topic.ecs_scheduled_task_failure.arn
    heartbeat              = var.sfn_heartbeat
    launch_type            = var.launch_type
    max_attempts           = var.sfn_max_attempts
    retry_interval         = var.sfn_retry_interval
    security_groups        = [data.aws_security_group.ecs.id]
    subnets                = data.aws_subnets.private.ids
    task_definition_family = replace(var.ecs_task_definition_arn, "/:\\d+$/", "")
    timeout                = var.sfn_timeout
  })

  tags = module.sfn_ecs_scheduled_task_label.tags
}

resource "aws_cloudwatch_event_target" "publish" {
  arn       = aws_sfn_state_machine.publish.arn
  rule      = aws_cloudwatch_event_rule.publish.name
  role_arn  = aws_iam_role.cloudwatch_scheduled_task_role.arn
  target_id = module.sfn_ecs_scheduled_task_event_target_label.id
}
