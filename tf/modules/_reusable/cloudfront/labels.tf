# Labels for the cloudfront module.

module "cloudfront_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  namespace   = var.namespace
  environment = var.environment
  name        = "cloudfront"

  labels_as_tags = ["namespace", "environment", "name"]
}

module "cloudfront_oac_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["oac"]

  context = module.cloudfront_label.context
}
