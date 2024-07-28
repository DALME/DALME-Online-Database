# Data sources for the cdn module.

data "aws_route53_zone" "tenant_zones" {
  for_each = toset(var.tenant_domains)
  name     = each.key
}
