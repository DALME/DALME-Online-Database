# Entrypoint for the sfn-ecs-scheduled-task module.
# https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/publishEvents.html#CronExpressions

locals {
  task_definition_family = replace(var.ecs_task_definition_arn, "/:\\d+$/", "")
}

resource "aws_sfn_state_machine" "this" {
  name     = module.sfn_ecs_scheduled_task_label.id
  role_arn = aws_iam_role.sfn_execution_role.arn

  definition = templatefile("${path.module}/files/scheduled-task.json.tmpl", {
    assign_public_ip       = var.assign_public_ip == true ? "ENABLED" : "DISABLED"
    backoff_rate           = var.backoff_rate
    cluster                = var.cluster
    container              = var.container
    failure_sns_topic      = var.failure_sns_topic
    heartbeat              = var.heartbeat
    launch_type            = var.launch_type
    max_attempts           = var.max_attempts
    retry_interval         = var.retry_interval
    security_groups        = var.security_groups
    subnets                = var.subnets
    task_definition_family = local.task_definition_family
    timeout                = var.timeout
  })

  tags = module.sfn_ecs_scheduled_task_label.tags
}

resource "aws_cloudwatch_event_rule" "this" {
  name                = module.sfn_ecs_scheduled_task_event_rule_label.id
  description         = var.description
  schedule_expression = var.schedule_expression
  state               = var.state

  tags = module.sfn_ecs_scheduled_task_event_rule_label.tags
}

resource "aws_cloudwatch_event_target" "this" {
  arn       = aws_sfn_state_machine.this.arn
  rule      = aws_cloudwatch_event_rule.this.name
  role_arn  = aws_iam_role.cloudwatch_event_role.arn
  target_id = module.sfn_ecs_scheduled_task_event_target_label.id
}
