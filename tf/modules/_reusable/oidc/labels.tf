# Labels for the oidc module.

module "oidc_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  namespace   = var.namespace
  environment = var.environment
  name        = var.provider_name

  labels_as_tags = ["namespace", "environment", "name"]
}

module "oidc_role_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  name = "oidc-github-actions-role"

  context = module.oidc_label.context
}
