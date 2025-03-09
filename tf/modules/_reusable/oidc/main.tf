# Resources for the oidc module.

locals {
  url = "https://token.actions.githubusercontent.com"
}

locals {
  thumbprint = data.tls_certificate.github.certificates[0].sha1_fingerprint
}

resource "aws_iam_openid_connect_provider" "github" {
  url             = local.url
  client_id_list  = ["sts.amazonaws.com"]
  thumbprint_list = [local.thumbprint]

  tags = module.oidc_label.tags
}
