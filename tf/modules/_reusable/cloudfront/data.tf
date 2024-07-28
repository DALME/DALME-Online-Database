# Data sources for the cloudfront module.

data "aws_route53_zone" "tenant_zones" {
  for_each = toset(local.all_tldrs)
  name     = each.key
}
