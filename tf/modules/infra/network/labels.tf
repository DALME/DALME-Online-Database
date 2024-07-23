# Labels for the network module.

module "network_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  namespace   = var.namespace
  environment = var.environment
  name        = "network"

  labels_as_tags = ["name"]
}

module "network_jh_asg_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["jump-host", "asg"]

  context = module.network_label.context
}

module "network_jh_role_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["jump-host", "role"]

  context = module.network_label.context
}

module "network_jh_policy_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["jump-host", "role", "policy"]

  context = module.network_label.context
}

module "network_jh_profile_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["jump-host", "profile"]

  context = module.network_label.context
}
