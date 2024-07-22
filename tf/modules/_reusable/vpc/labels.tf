# Labels for the vpc module.

module "vpc_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  namespace   = var.namespace
  environment = var.environment
  name        = "vpc"

  labels_as_tags = ["namespace", "environment", "name"]
}

module "vpc_eip_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["eip"]

  context = module.vpc_label.context
}

module "vpc_flow_logs_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["flow", "logs"]

  context = module.vpc_label.context
}

module "vpc_igw_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["igw"]

  context = module.vpc_label.context
}

module "vpc_ngw_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["ngw"]

  context = module.vpc_label.context
}

module "vpc_rt_private_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes         = ["rt"]
  additional_tag_map = { Scope = "private" }

  context = module.vpc_label.context
}

module "vpc_rt_public_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes         = ["rt"]
  additional_tag_map = { Scope = "public" }

  context = module.vpc_label.context
}

module "vpc_subnet_private_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes         = ["subnet"]
  additional_tag_map = { Scope = "private" }

  context = module.vpc_label.context
}

module "vpc_subnet_public_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes         = ["subnet"]
  additional_tag_map = { Scope = "public" }

  context = module.vpc_label.context
}
