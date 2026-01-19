# Entrypoint for the alb module.

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
  certificate_arn   = var.certificate_arn
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
