# Labels for the ec2-instance module.

module "ec2_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  namespace   = var.namespace
  environment = var.environment
  name        = "ec2"
  attributes  = [var.name]

  labels_as_tags = ["namespace", "environment", "name"]
}

module "ec2_label_sg" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["security", "group"]

  context = module.ec2_label.context
}
