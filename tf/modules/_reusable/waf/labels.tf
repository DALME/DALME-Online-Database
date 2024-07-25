# Labels for the waf module.

module "waf_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  namespace   = var.namespace
  environment = var.environment
  name        = "waf"

  labels_as_tags = ["namespace", "environment", "name"]
}

module "waf_ipv4_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["ip", "set", "v4"]

  context = module.waf_label.context
}

module "waf_ipv6_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["ip", "set", "v6"]

  context = module.waf_label.context
}
