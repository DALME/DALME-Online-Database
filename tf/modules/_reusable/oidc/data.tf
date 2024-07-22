# Data sources for the oidc module.

data "tls_certificate" "github" {
  url = local.url
}
