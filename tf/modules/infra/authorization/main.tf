# Entrypoint for the authorization module.

module "oidc" {
  source = "../..//_reusable/oidc/"

  environment        = var.environment
  gha_oidc_role_name = var.gha_oidc_role_name
  oidc_allowed       = var.oidc_allowed
  namespace          = var.namespace
}
