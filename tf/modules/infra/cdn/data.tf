# Data sources for the cdn module.
#
# Any dependencies between this node and ancestors on the environment DAG
# should be resolved here and then passed to resources in this module.

data "aws_lb" "this" {
  tags = {
    Namespace   = var.namespace
    Environment = var.environment
  }
}

data "aws_route53_zone" "tenant_zones" {
  for_each = toset(var.tenant_domains)
  name     = each.key
}

data "aws_wafv2_web_acl" "this" {
  name  = "${var.namespace}-${var.environment}-waf-cloudfront"
  scope = "CLOUDFRONT"
}
