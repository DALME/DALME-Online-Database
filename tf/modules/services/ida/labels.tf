# Labels for the ida module.

module "ida_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  namespace   = var.namespace
  environment = var.environment
  name        = "ida"

  labels_as_tags = ["namespace", "environment", "name"]
}

module "ida_ecs_task_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["ecs", "task"]

  context = module.ida_label.context
}

module "ida_ecs_task_role_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["role"]

  context = module.ida_ecs_task_label.context
}

module "ida_ecs_task_policy_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["policy"]

  context = module.ida_ecs_task_label.context
}

module "ida_ecs_task_definition_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["definition", "web"]

  context = module.ida_ecs_task_label.context
}

module "ida_ecs_task_execution_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["execution"]

  context = module.ida_ecs_task_label.context
}

module "ida_ecs_task_execution_role_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["role"]

  context = module.ida_ecs_task_execution_label.context
}

module "ida_ecs_task_execution_policy_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["policy"]

  context = module.ida_ecs_task_execution_label.context
}

module "ida_log_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["log"]

  context = module.ida_label.context
}

module "ida_log_group_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["group"]
  delimiter  = "/"

  context = module.ida_log_label.context
}

module "ida_log_stream_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["stream"]

  context = module.ida_log_label.context
}

module "ida_log_group_web_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["web"]
  delimiter  = "/"

  context = module.ida_log_group_label.context
}

module "ida_log_stream_web_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["web"]

  context = module.ida_log_stream_label.context
}

module "ida_log_group_proxy_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["proxy"]
  delimiter  = "/"

  context = module.ida_log_group_label.context
}

module "ida_log_stream_proxy_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["proxy"]

  context = module.ida_log_stream_label.context
}

module "ida_sns_ecs_scheduled_task_failure_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["sns", "topic", "ecs", "scheduled", "task", "failure"]

  context = module.ida_label.context
}

module "ida_sfn_ecs_scheduled_task_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["scheduled"]

  context = module.ida_ecs_task_label.context
}

module "ida_sfn_ecs_scheduled_task_cleartokens_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["cleartokens"]

  context = module.ida_sfn_ecs_scheduled_task_label.context
}

module "ida_sfn_ecs_scheduled_task_publish_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["publish"]

  context = module.ida_sfn_ecs_scheduled_task_label.context
}
