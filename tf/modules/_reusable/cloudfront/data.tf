# Data sources for the cloudfront module.

data "aws_route53_zone" "tenant_zones" {
  for_each = toset(var.tenant_domains)
  name     = each.key
}
