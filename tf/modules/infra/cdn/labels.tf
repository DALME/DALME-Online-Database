# Labels for the cdn module.

module "cdn_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  namespace   = var.namespace
  environment = var.environment
  name        = "cdn"

  labels_as_tags = ["namespace", "environment", "name"]
}

module "cdn_certificate_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["ssl", "certificate"]

  context = module.cdn_label.context
}

module "cdn_access_logs_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["access", "logs"]

  context = module.cdn_label.context
}

module "cloudfront_function_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  namespace   = var.namespace
  environment = var.environment
  name        = "cloudfront"
  attributes  = ["function"]

  labels_as_tags = ["namespace", "environment", "name"]
}

module "cloudfront_function_label_vr" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["viewer", "request"]

  context = module.cloudfront_function_label.context
}

module "cdn_oac_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["oac"]

  context = module.cdn_label.context
}
