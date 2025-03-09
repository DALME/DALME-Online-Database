# Entrypoint for the alb module.

locals {
  all_tldrs                 = concat([var.domain], var.additional_domains)
  wildcard_domains          = [for domain in local.all_tldrs : "*.${domain}"]
  subject_alternative_names = concat(var.additional_domains, local.wildcard_domains)
  zone_ids = {
    for zone in data.aws_route53_zone.tenant_zones : zone.name => zone.zone_id
  }
}

resource "aws_acm_certificate" "alb" {
  domain_name               = var.domain
  subject_alternative_names = local.subject_alternative_names
  validation_method         = "DNS"

  lifecycle {
    create_before_destroy = true
  }

  tags = module.alb_certificate_label.tags
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

resource "aws_security_group" "alb" {
  description = "Controls access to the ALB."
  name_prefix = "${module.alb_sg_label.id}-"
  vpc_id      = var.vpc_id

  lifecycle {
    create_before_destroy = true
  }

  tags = module.alb_sg_label.tags
}

resource "aws_lb" "this" {
  # Note, internal must be set to false if you want the load balancer to be
  # connected to a Cloudfront origin.
  # tfsec:ignore:aws-elb-alb-not-public
  internal = var.internal

  drop_invalid_header_fields = true
  enable_deletion_protection = false
  load_balancer_type         = "application"
  security_groups            = [aws_security_group.alb.id]
  subnets                    = var.subnets

  depends_on = [
    aws_acm_certificate_validation.alb
  ]

  # Be sure to disable access logs before you delete the bucket that you
  # configured for access logs. Otherwise, if there is a new bucket with the
  # same name and the required bucket policy but created in an AWS account that
  # you don't own, Elastic Load Balancing could write the access logs for your
  # load balancer to this new bucket.
  access_logs {
    bucket  = var.log_destination
    enabled = var.logging_enabled
    prefix  = var.log_prefix
  }

  lifecycle {
    ignore_changes = [
      subnets
    ]
  }

  tags = module.alb_label.tags
}

resource "aws_lb_target_group" "this" {
  port        = var.alb_port
  protocol    = "HTTP"
  target_type = "ip"
  vpc_id      = var.vpc_id

  load_balancing_algorithm_type = "least_outstanding_requests"

  health_check {
    healthy_threshold   = var.health_check.threshold
    interval            = var.health_check.interval
    matcher             = var.health_check.matcher
    path                = var.health_check.path
    protocol            = "HTTP"
    timeout             = var.health_check.timeout
    unhealthy_threshold = var.health_check.unhealthy_threshold
  }

  tags = module.alb_tg_label.tags
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.this.id
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

  tags = module.alb_http_label.tags
}

resource "aws_lb_listener" "https" {
  certificate_arn   = aws_acm_certificate.alb.arn
  load_balancer_arn = aws_lb.this.id
  port              = var.ssl_port
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-TLS13-1-2-2021-06"

  default_action {
    target_group_arn = aws_lb_target_group.this.id
    type             = "forward"
  }

  tags = module.alb_https_label.tags
}
