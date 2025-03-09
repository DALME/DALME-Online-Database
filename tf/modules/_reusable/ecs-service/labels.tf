# Labels for the ecs-service module.

module "ecs_service_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  namespace   = var.namespace
  environment = var.environment
  name        = "ecs"
  attributes  = ["service"]

  labels_as_tags = ["namespace", "environment", "name"]
}

module "ecs_service_autoscaling_cpu_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["autoscaling", "cpu"]

  context = module.ecs_service_label.context
}

module "ecs_service_autoscaling_memory_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["autoscaling", "memory"]

  context = module.ecs_service_label.context
}

module "ecs_service_autoscaling_target_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["autoscaling", "target"]

  context = module.ecs_service_label.context
}
