# Data sources for the alb module.

data "aws_route53_zone" "main" {
  name = var.domain
}
