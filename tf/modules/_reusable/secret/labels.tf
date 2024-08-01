# Labels for the secret module.

module "secret_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  namespace   = var.namespace
  environment = var.environment
  name        = "secret"

  labels_as_tags = ["namespace", "environment", "name"]
}
