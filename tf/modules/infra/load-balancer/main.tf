# Entrypoint for the load-balancer module.

locals {
  log_prefix = "alb"
}

# Be sure to disable access logs on the ALB before you delete the bucket that
# you configured for access logs. Otherwise, if there is a new bucket with the
# same name and the required bucket policy but created in an AWS account that
# you don't own, Elastic Load Balancing could write the access logs for your
# load balancer to this new bucket.
module "alb_access_logs" {
  source = "../..//_reusable/bucket/"

  acl                      = "log-delivery-write"
  aws_account              = var.aws_account
  control_object_ownership = true
  environment              = var.environment
  force_destroy            = var.force_destroy
  name                     = "alb-logs"
  namespace                = var.namespace
  object_ownership         = "ObjectWriter"

  lifecycle_rule = [
    {
      id     = "ssm"
      status = "Enabled"

      filter = {
        prefix = "/"
      }

      expiration = {
        days = 90
      }

      noncurrent_version_expiration = {
        noncurrent_days = 90
      }

      noncurrent_version_transition = {
        noncurrent_days = 30
        storage_class   = "STANDARD_IA"
      }
    }
  ]

  server_side_encryption_configuration = {
    rule = {
      apply_server_side_encryption_by_default = {
        sse_algorithm = "AES256"
      }
      bucket_key_enabled = true
    }
  }

  versioning = {
    enabled = true
  }
}

module "alb" {
  source = "../..//_reusable/alb/"

  additional_domains = var.additional_domains
  alb_port           = var.alb_port
  dns_ttl            = var.dns_ttl
  domain             = var.domain
  environment        = var.environment
  force_destroy      = var.force_destroy
  health_check       = var.health_check
  internal           = var.internal
  log_destination    = module.alb_access_logs.bucket_id
  log_prefix         = local.log_prefix
  logging_enabled    = true
  namespace          = var.namespace
  ssl_port           = var.ssl_port
  subnets            = data.aws_subnets.public.ids
  vpc_id             = data.aws_vpc.this.id
}

resource "aws_vpc_security_group_ingress_rule" "alb_ingress_https" {
  description       = "Allow incoming HTTPS traffic to the ALB from Cloudfront only."
  security_group_id = module.alb.security_group_id

  ip_protocol = var.protocol
  from_port   = var.ssl_port
  to_port     = var.ssl_port

  prefix_list_id = data.aws_ec2_managed_prefix_list.cloudfront.id

  tags = module.alb_sg_ingress_https_label.tags
}

# NOTE: AWS makes these rules by default for any security group but terraform
# disables them by default. I am not sure why tfsec considers this an issue.
resource "aws_vpc_security_group_egress_rule" "alb_egress" {
  description       = "Explicit ALLOW ALL outbound rule."
  security_group_id = module.alb.security_group_id

  ip_protocol = "-1"
  from_port   = 0
  to_port     = 0

  # tfsec:ignore:aws-ec2-no-public-egress-sgr
  cidr_ipv4 = var.cidr_blocks

  tags = module.alb_sg_egress_label.tags
}
