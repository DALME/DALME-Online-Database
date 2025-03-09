# Labels for the load-balancer module.

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
