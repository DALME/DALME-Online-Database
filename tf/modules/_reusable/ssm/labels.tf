# Labels for the ssm module.

module "ssm_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  namespace   = var.namespace
  environment = var.environment
  name        = "ssm"

  labels_as_tags = ["namespace", "environment", "name"]
}

module "ssm_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["kms", "key"]

  context = module.ssm_label.tags
}
