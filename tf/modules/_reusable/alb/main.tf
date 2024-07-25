# Entrypoint for the alb module.

resource "aws_acm_certificate" "alb" {
  domain_name               = var.domain
  subject_alternative_names = ["*.${var.domain}"]
  validation_method         = "DNS"

  lifecycle {
    create_before_destroy = true
  }

  tags = module.alb_certificate_label.tags
}

resource "aws_route53_record" "alb" {
  for_each = {
    for dvo in aws_acm_certificate.alb.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }

  allow_overwrite = true
  name            = each.value.name
  records         = [each.value.record]
  ttl             = var.dns_ttl
  type            = each.value.type
  zone_id         = data.aws_route53_zone.main.zone_id
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
  drop_invalid_header_fields = true
  enable_deletion_protection = false
  load_balancer_type         = "application"
  security_groups            = [aws_security_group.alb.id]
  subnets                    = var.subnets

  # The load balancer must be public to connect to Cloudfront.
  # tfsec:ignore:aws-elb-alb-not-public
  internal = false

  depends_on = [
    aws_acm_certificate_validation.alb
  ]

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
