# Labels for the load-balancer module.

module "alb_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  namespace   = var.namespace
  environment = var.environment
  name        = "alb"

  labels_as_tags = ["namespace", "environment", "name"]
}

module "alb_sg_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["security", "group"]

  context = module.alb_label.context
}

module "alb_sg_egress_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["egress"]

  context = module.alb_sg_label.context
}

module "alb_sg_ingress_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["ingress"]

  context = module.alb_sg_label.context
}

module "alb_sg_ingress_https_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["https"]

  context = module.alb_sg_ingress_label.context
}
