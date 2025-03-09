# IAM roles and permissions for the load-balancer module.

locals {
  arn = "arn:aws:s3:::${module.alb_access_logs.bucket_id}/${local.log_prefix}/AWSLogs/${var.aws_account}/*"
}

data "aws_iam_policy_document" "alb_logs" {
  statement {
    effect = "Allow"
    actions = [
      "s3:PutObject",
    ]
    resources = [
      local.arn,
    ]

    principals {
      type        = "AWS"
      identifiers = [data.aws_elb_service_account.this.arn]
    }
  }
}

resource "aws_s3_bucket_policy" "alb_logs" {
  bucket = module.alb_access_logs.bucket_id
  policy = data.aws_iam_policy_document.alb_logs.json
}
