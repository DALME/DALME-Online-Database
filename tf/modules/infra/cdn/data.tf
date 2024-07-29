# Data sources for the cdn module.

data "aws_lb" "this" {
  tags = {
    Name      = "${var.namespace}-${var.environment}-alb"
    Namespace = var.namespace
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
