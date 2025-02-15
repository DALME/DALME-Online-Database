# IAM roles and permissions for the cdn module.
data "aws_iam_policy_document" "oac_assets" {
  statement {
    actions = [
      "s3:GetObject",
      "s3:GetObjectVersion",
    ]

    condition {
      test     = "StringEquals"
      variable = "aws:SourceArn"
      values   = [module.cloudfront.arn]
    }

    principals {
      type        = "Service"
      identifiers = ["cloudfront.amazonaws.com"]
    }

    resources = [
      "${module.assets.bucket_arn}/*",
    ]
  }
}

data "aws_iam_policy_document" "oac_staticfiles" {
  statement {
    actions = [
      "s3:GetObject",
      "s3:GetObjectAcl",
      "s3:GetObjectVersion",
      "s3:ListBucket",
    ]

    condition {
      test     = "StringEquals"
      variable = "aws:SourceArn"
      values   = [module.cloudfront.arn]
    }

    principals {
      type        = "Service"
      identifiers = ["cloudfront.amazonaws.com"]
    }

    resources = [
      module.staticfiles.bucket_arn,
      "${module.staticfiles.bucket_arn}/*",
    ]
  }
}

resource "aws_s3_bucket_policy" "oac_assets" {
  bucket = module.assets.bucket_id
  policy = data.aws_iam_policy_document.oac_assets.json
}

resource "aws_s3_bucket_policy" "oac_staticfiles" {
  bucket = module.staticfiles.bucket_id
  policy = data.aws_iam_policy_document.oac_staticfiles.json
}
