# Labels for the load-balancer module.

module "load_balancer_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  namespace   = var.namespace
  environment = var.environment
  name        = "load-balancer"

  labels_as_tags = ["namespace", "environment", "name"]
}

module "load_balancer_certificate_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["ssl", "certificate"]

  context = module.load_balancer_label.context
}

module "alb_sg_egress_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["egress"]

  context = module.alb.security_group_label_context
}

module "alb_sg_ingress_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["ingress"]

  context = module.alb.security_group_label_context
}

module "alb_sg_ingress_https_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["https"]

  context = module.alb_sg_ingress_label.context
}
