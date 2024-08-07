# Labels for the sfn-ecs-scheduled-task module.

module "sfn_ecs_scheduled_task_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  namespace   = var.namespace
  environment = var.environment
  name        = "sfn"
  attributes  = ["ecs", "scheduled", "task", var.name]

  labels_as_tags = ["namespace", "environment", "name"]
}

module "sfn_ecs_scheduled_task_execution_role_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["execution", "role"]

  context = module.sfn_ecs_scheduled_task_label.context
}

module "sfn_ecs_scheduled_task_execution_policy_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["execution", "policy"]

  context = module.sfn_ecs_scheduled_task_label.context
}

module "sfn_ecs_scheduled_task_event_rule_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["event", "rule"]

  context = module.sfn_ecs_scheduled_task_label.context
}

module "sfn_ecs_scheduled_task_event_target_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["event", "target"]

  context = module.sfn_ecs_scheduled_task_label.context
}

module "sfn_ecs_scheduled_task_sns_topic_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["sns", "topic", "failure"]

  context = module.sfn_ecs_scheduled_task_label.context
}
