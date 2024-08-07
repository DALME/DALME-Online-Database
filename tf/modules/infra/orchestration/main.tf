# Entrypoint for the orchestration module.

module "ecs_cluster" {
  source = "../..//_reusable/ecs-cluster/"

  environment                        = var.environment
  capacity_providers                 = var.capacity_providers
  default_capacity_provider_strategy = var.default_capacity_provider_strategy
  namespace                          = var.namespace
  vpc_id                             = data.aws_vpc.this.id
}

resource "aws_security_group_rule" "ecs_ingress_alb" {
  security_group_id        = module.ecs_cluster.security_group_id
  type                     = "ingress"
  description              = "Allow incoming traffic to ECS from the ALB."
  protocol                 = "tcp"
  from_port                = var.proxy_port
  to_port                  = var.proxy_port
  source_security_group_id = data.aws_security_group.alb.id
}

# This is reversed in polarity than the above but it simplifies the dependency
# graph to have it here (there would be a cycle otherwise).
resource "aws_security_group_rule" "postgres_ingress_ecs" {
  security_group_id        = data.aws_security_group.postgres.id
  type                     = "ingress"
  description              = "Allow incoming traffic to postgres from ECS."
  protocol                 = "tcp"
  from_port                = var.postgres_port
  to_port                  = var.postgres_port
  source_security_group_id = module.ecs_cluster.security_group_id
}

# NOTE: AWS makes these rules by default for any security group but terraform
# disables them, so I am not sure why tfsec considers this an issue.
resource "aws_security_group_rule" "ecs_egress" {
  security_group_id = module.ecs_cluster.security_group_id
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
