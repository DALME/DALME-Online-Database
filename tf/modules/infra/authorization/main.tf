# Entrypoint for the authorization module.

module "oidc" {
  source = "../..//_reusable/oidc/"

  environment = var.environment
  allowed     = var.allowed_oidc
  namespace   = var.namespace
}
