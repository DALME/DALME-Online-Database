# Labels for the authorization module.

module "oidc_policy" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  namespace   = var.namespace
  environment = var.environment
  name        = "${var.gha_oidc_role_name}-policy"

  labels_as_tags = ["name"]
}

module "oidc_policy_one" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["one"]

  context = module.oidc_policy.context
}

module "oidc_policy_two" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["two"]

  context = module.oidc_policy.context
}
