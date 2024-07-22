# Labels for the bucket module.

module "bucket_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  namespace   = var.namespace
  environment = var.environment
  name        = var.name
  attributes  = [var.aws_account]

  labels_as_tags = ["namespace", "environment", "name"]
}
