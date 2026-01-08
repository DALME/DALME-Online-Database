# Data sources for the load-balancer module.
#
# Any dependencies between this node and ancestors on the environment DAG
# should be resolved here and then passed to resources in this module.

data "aws_route53_zone" "tenant_zones" {
  provider = aws.dns_account

  for_each = toset(local.zone_domains)
  name     = each.key
}

data "aws_ec2_managed_prefix_list" "cloudfront" {
  name = "com.amazonaws.global.cloudfront.origin-facing"
}

data "aws_elb_service_account" "this" {}

data "aws_subnets" "public" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.this.id]
  }

  tags = {
    Environment = var.environment
    Namespace   = var.namespace
    Scope       = "public"
  }
}

data "aws_vpc" "this" {
  tags = {
    Environment = var.environment
    Namespace   = var.namespace
  }
}
