# Labels for the ecr module.

module "ecr_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  namespace   = var.namespace
  environment = var.environment
  name        = "ecr"
  attributes  = [local.name]

  labels_as_tags = ["namespace", "environment", "name"]
}
