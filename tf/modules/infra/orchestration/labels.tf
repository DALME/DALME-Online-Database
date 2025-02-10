# Labels for the orchestration module.

module "ecs_sg_egress_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["egress"]

  context = module.ecs_cluster.security_group_label_context
}

module "ecs_sg_ingress_alb_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["ingress", "alb"]

  context = module.ecs_cluster.security_group_label_context
}

module "ecs_sg_ingress_postgres_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["ingress", "postgres"]

  context = module.ecs_cluster.security_group_label_context
}

module "opensearch_sg_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  namespace   = var.namespace
  environment = var.environment
  name        = "opensearch"
  attributes  = ["security", "group"]

  labels_as_tags = ["namespace", "environment", "name"]
}

module "opensearch_sg_ingress_ecs_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["ingress", "ecs", "cluster"]

  context = module.opensearch_sg_label.context
}
