# IAM roles and permissions for the oidc module.

data "aws_iam_policy_document" "this" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRoleWithWebIdentity"]

    principals {
      identifiers = [aws_iam_openid_connect_provider.github.arn]
      type        = "Federated"
    }

    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:aud"
      values   = ["sts.amazonaws.com"]
    }

    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:sub"
      values = concat(
        [
          for item in var.oidc_allowed :
          "repo:${item["org"]}/${item["repo"]}:pull_request"
        ],
        [
          for item in var.oidc_allowed :
          "repo:${item["org"]}/${item["repo"]}:ref:refs/heads/${item["branch"]}"
        ],
      )
    }
  }
}

resource "aws_iam_role" "this" {
  name               = module.oidc_role.id
  assume_role_policy = data.aws_iam_policy_document.this.json

  tags = module.oidc_role.tags
}
