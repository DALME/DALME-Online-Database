# Labels for the cdn module.

module "cdn_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  namespace   = var.namespace
  environment = var.environment
  name        = "cdn"

  labels_as_tags = ["namespace", "environment", "name"]
}

module "cdn_access_logs_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["access", "logs"]

  context = module.cdn_label.context
}
