# IAM roles and permissions for the cdn module.
data "aws_iam_policy_document" "oac_assets" {
  statement {
    actions = [
      "s3:GetObject",
      "s3:GetObjectVersion",
    ]
    resources = [
      "${module.assets.s3_bucket_arn}/*",
    ]

    principals {
      type        = "Service"
      identifiers = ["cloudfront.amazonaws.com"]
    }

    condition {
      test     = "StringEquals"
      variable = "aws:SourceArn"
      values   = [aws_cloudfront_distribution.main.arn]
    }
  }
}

data "aws_iam_policy_document" "oac_staticfiles" {
  statement {
    actions = [
      "s3:GetObject",
      "s3:GetObjectVersion",
    ]
    resources = [
      "${module.staticfiles.s3_bucket_arn}/*",
    ]

    principals {
      type        = "Service"
      identifiers = ["cloudfront.amazonaws.com"]
    }

    condition {
      test     = "StringEquals"
      variable = "aws:SourceArn"
      values   = [aws_cloudfront_distribution.main.arn]
    }
  }
}

resource "aws_s3_bucket_policy" "oac_assets" {
  bucket = module.assets.s3_bucket_id
  policy = data.aws_iam_policy_document.oac_assets.json
}

resource "aws_s3_bucket_policy" "oac_staticfiles" {
  bucket = module.staticfiles.s3_bucket_id
  policy = data.aws_iam_policy_document.oac_staticfiles.json
}
