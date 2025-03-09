# Labels for the rds module.

module "rds_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  namespace   = var.namespace
  environment = var.environment
  name        = "rds"
  attributes  = [var.engine, var.engine_version]

  labels_as_tags = ["namespace", "environment", "name"]
}

module "rds_pg_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["parameter", "group"]

  context = module.rds_label.context
}

module "rds_sg_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["security", "group"]

  context = module.rds_label.context
}

module "rds_sbng_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["subnet", "group"]

  context = module.rds_label.context
}
