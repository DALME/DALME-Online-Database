# Labels for the ecs-cluster module.

module "ecs_cluster_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  namespace   = var.namespace
  environment = var.environment
  name        = "ecs"
  attributes  = ["cluster"]

  labels_as_tags = ["namespace", "environment", "name"]
}

module "ecs_cluster_sg_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["security", "group"]

  context = module.ecs_cluster_label.context
}
