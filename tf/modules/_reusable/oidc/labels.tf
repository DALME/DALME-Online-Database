# Labels for the oidc module.

module "oidc" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  namespace   = var.namespace
  environment = var.environment
  name        = "oidc-provider"

  labels_as_tags = ["name"]
}

module "oidc_role" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  name = var.gha_oidc_role_name

  context = module.oidc.context
}
