# IAM roles and permissions for the clodufront module.

data "aws_iam_policy_document" "oac_assets" {
  statement {
    actions = [
      "s3:GetObject",
      "s3:GetObjectVersion",
      "s3:ListBucket",
    ]
    resources = [
      module.assets.s3_bucket_arn,
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
      "s3:ListBucket",
    ]
    resources = [
      module.staticfiles.s3_bucket_arn,
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

data "aws_iam_policy_document" "public_staticfiles" {
  statement {
    actions = [
      "s3:GetObject",
      "s3:GetObjectVersion",
      "s3:ListBucket",
    ]
    resources = [
      module.staticfiles.s3_bucket_arn,
      "${module.staticfiles.s3_bucket_arn}/*",
    ]

    principals {
      type        = "*"
      identifiers = ["*"]
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

resource "aws_s3_bucket_policy" "public_staticfiles" {
  bucket = module.staticfiles.s3_bucket_id
  policy = data.aws_iam_policy_document.public_staticfiles.json
}
