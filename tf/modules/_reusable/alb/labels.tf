# Labels for the alb module.

module "alb_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  namespace   = var.namespace
  environment = var.environment
  name        = "alb"

  labels_as_tags = ["namespace", "environment", "name"]
}

module "alb_http_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["http", "listener"]

  context = module.alb_label.context
}

module "alb_https_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["https", "listener"]

  context = module.alb_label.context
}


module "alb_sg_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["security", "group"]

  context = module.alb_label.context
}

module "alb_tg_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["target", "group"]

  context = module.alb_label.context
}
