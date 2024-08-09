# Entrypoint for the load-balancer module.

module "alb" {
  source = "../..//_reusable/alb/"

  alb_port     = var.alb_port
  dns_ttl      = var.dns_ttl
  domain       = var.domain
  environment  = var.environment
  health_check = var.health_check
  internal     = var.internal
  namespace    = var.namespace
  ssl_port     = var.ssl_port
  subnets      = data.aws_subnets.public.ids
  vpc_id       = data.aws_vpc.this.id
}

resource "aws_security_group_rule" "alb_ingress_http" {
  security_group_id = module.alb.security_group_id
  description       = "Inbound HTTP to the ALB."
  type              = "ingress"
  protocol          = var.protocol
  from_port         = var.proxy_port
  to_port           = var.proxy_port
  cidr_blocks       = [var.cidr_blocks]
  ipv6_cidr_blocks  = [var.ipv6_cidr_blocks]
}

resource "aws_security_group_rule" "alb_ingress_https" {
  security_group_id = module.alb.security_group_id
  description       = "Inbound HTTPS to the ALB."
  type              = "ingress"
  protocol          = var.protocol
  from_port         = var.ssl_port
  to_port           = var.ssl_port
  cidr_blocks       = [var.cidr_blocks]
  ipv6_cidr_blocks  = [var.ipv6_cidr_blocks]
}

# NOTE: AWS makes these rules by default for any security group but terraform
# disables them, so I am not sure why tfsec considers this an issue.
resource "aws_security_group_rule" "alb_egress" {
  security_group_id = module.alb.security_group_id
  type              = "egress"
  description       = "Explicit ALLOW ALL outbound rule."
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  # tfsec:ignore:aws-ec2-no-public-egress-sgr
  cidr_blocks = ["0.0.0.0/0"]
  # tfsec:ignore:aws-ec2-no-public-egress-sgr
  ipv6_cidr_blocks = ["::/0"]
}
