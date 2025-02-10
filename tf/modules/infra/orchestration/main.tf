# Entrypoint for the orchestration module.

module "ecs_cluster" {
  source = "../..//_reusable/ecs-cluster/"

  environment                        = var.environment
  capacity_providers                 = var.capacity_providers
  default_capacity_provider_strategy = var.default_capacity_provider_strategy
  namespace                          = var.namespace
  vpc_id                             = data.aws_vpc.this.id
}

resource "aws_vpc_security_group_ingress_rule" "ecs_ingress_alb" {
  description       = "Allow incoming traffic to ECS from the ALB."
  security_group_id = module.ecs_cluster.security_group_id

  ip_protocol = "tcp"
  from_port   = var.proxy_port
  to_port     = var.proxy_port

  referenced_security_group_id = data.aws_security_group.alb.id

  tags = module.ecs_sg_ingress_alb_label.tags
}

resource "aws_vpc_security_group_ingress_rule" "ecs_ingress_postgres" {
  description       = "Allow incoming traffic to postgres from ECS."
  security_group_id = data.aws_security_group.postgres.id

  ip_protocol = "tcp"
  from_port   = var.postgres_port
  to_port     = var.postgres_port

  referenced_security_group_id = module.ecs_cluster.security_group_id

  tags = module.ecs_sg_ingress_postgres_label.tags
}

# TODO: We also need to think about SSM for kibana?
resource "aws_vpc_security_group_ingress_rule" "opensearch_ingress_ecs" {
  description       = "Allow incoming traffic to Opensearch from ECS."
  security_group_id = data.aws_security_group.opensearch.id

  ip_protocol = "tcp"
  from_port   = var.opensearch_port
  to_port     = var.opensearch_port

  referenced_security_group_id = module.ecs_cluster.security_group_id

  tags = module.opensearch_sg_ingress_ecs_label.tags
}

# NOTE: AWS makes these rules by default for any security group but terraform
# disables them by default. I am not sure why tfsec considers this an issue.
resource "aws_vpc_security_group_egress_rule" "ecs_egress" {
  description       = "Explicit ALLOW ALL outbound rule."
  security_group_id = module.ecs_cluster.security_group_id

  ip_protocol = "-1"
  from_port   = 0
  to_port     = 0

  # tfsec:ignore:aws-ec2-no-public-egress-sgr
  cidr_ipv4 = "0.0.0.0/0"

  tags = module.ecs_sg_egress_label.tags
}
