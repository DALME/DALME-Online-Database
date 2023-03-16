# Terraform definitions for the alb module.

terraform {
  required_version = "~> 1.3"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.14.0"
    }
  }
}

// Certificate
locals {
  domain                      = var.tenant_domains[0]
  alt_domains                 = slice(var.tenant_domains, 1, length(var.tenant_domains))
  wildcard_domains            = [for domain in var.tenant_domains : "*.${domain}"]
  subject_alternative_domains = concat(local.alt_domains, local.wildcard_domains)
}

resource "aws_acm_certificate" "alb" {
  domain_name               = local.domain
  subject_alternative_names = local.subject_alternative_domains
  validation_method         = "DNS"

  lifecycle {
    create_before_destroy = true
  }

  tags = {
    Name = "${var.service}-alb-certificate-${var.environment}"
  }
}

data "aws_route53_zone" "tenant_zones" {
  for_each = toset(var.tenant_domains)
  name     = each.key
}

locals {
  zone_ids = {
    for zone in data.aws_route53_zone.tenant_zones : zone.name => zone.zone_id
  }
}

resource "aws_route53_record" "alb" {
  for_each = {
    for dvo in aws_acm_certificate.alb.domain_validation_options : dvo.domain_name => {
      name    = dvo.resource_record_name
      record  = dvo.resource_record_value
      type    = dvo.resource_record_type
      zone_id = local.zone_ids[dvo.domain_name]
    } if !strcontains(dvo.domain_name, "*.")
  }

  allow_overwrite = true
  name            = each.value.name
  records         = [each.value.record]
  ttl             = var.dns_ttl
  type            = each.value.type
  zone_id         = each.value.zone_id
}

resource "aws_acm_certificate_validation" "alb" {
  certificate_arn = aws_acm_certificate.alb.arn
  validation_record_fqdns = [
    for record in aws_route53_record.alb : record.fqdn
  ]
}

// Load balancer
resource "aws_lb" "main" {
  name                       = "${var.service}-alb-${var.environment}"
  drop_invalid_header_fields = true
  enable_deletion_protection = false
  # tfsec:ignore:aws-elb-alb-not-public
  internal           = false
  load_balancer_type = "application"
  security_groups    = var.security_groups
  subnets            = var.subnets

  depends_on = [
    aws_acm_certificate_validation.alb
  ]

  lifecycle {
    ignore_changes = [subnets]
  }

  tags = {
    Name = "${var.service}-alb-${var.environment}"
  }
}

resource "aws_lb_target_group" "main" {
  name        = "${var.service}-alb-tg-${var.environment}"
  port        = var.alb_port
  protocol    = "HTTP"
  vpc_id      = var.vpc_id
  target_type = "ip"

  load_balancing_algorithm_type = "least_outstanding_requests"

  health_check {
    healthy_threshold   = var.health_check_threshold
    interval            = var.health_check_interval
    matcher             = var.health_check_matcher
    path                = var.health_check_path
    protocol            = "HTTP"
    timeout             = var.health_check_timeout
    unhealthy_threshold = var.health_check_unhealthy_threshold
  }

  tags = {
    Name = "${var.service}-alb-tg-${var.environment}"
  }
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.main.id
  port              = var.alb_port
  protocol          = "HTTP"

  default_action {
    type = "redirect"

    redirect {
      port        = var.ssl_port
      protocol    = "HTTPS"
      status_code = "HTTP_301"
    }
  }

  tags = {
    Name = "${var.service}-alb-listener-http-${var.environment}"
  }
}

resource "aws_lb_listener" "https" {
  load_balancer_arn = aws_lb.main.id
  port              = var.ssl_port
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-TLS13-1-2-2021-06"
  certificate_arn   = aws_acm_certificate.alb.arn

  default_action {
    target_group_arn = aws_lb_target_group.main.id
    type             = "forward"
  }

  tags = {
    Name = "${var.service}-alb-listener-https-${var.environment}"
  }
}

# resource "aws_lb_listener_certificate" "example" {
#   listener_arn    = "${aws_lb_listener.front_end.arn}"
#   certificate_arn = "${aws_acm_certificate.example.arn}"
# }
