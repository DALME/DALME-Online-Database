# Labels for the security module.

module "kms_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  namespace   = var.namespace
  environment = var.environment
  name        = "kms"
  attributes  = ["key", "global"]

  labels_as_tags = ["name"]
}
