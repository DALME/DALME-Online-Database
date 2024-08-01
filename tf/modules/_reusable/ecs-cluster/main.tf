# Entrypoint for the ecs-cluster module.

resource "aws_ecs_cluster" "this" {
  name = module.ecs_cluster_label.id

  setting {
    name  = "containerInsights"
    value = "enabled"
  }

  tags = module.ecs_cluster_label.tags
}

resource "aws_ecs_cluster_capacity_providers" "this" {
  cluster_name = aws_ecs_cluster.this.name

  capacity_providers = var.capacity_providers

  default_capacity_provider_strategy {
    base              = var.default_capacity_provider_strategy.base
    weight            = var.default_capacity_provider_strategy.weight
    capacity_provider = var.default_capacity_provider_strategy.capacity_provider
  }
}

resource "aws_security_group" "ecs" {
  description = "Controls access to the ECS cluster."
  name_prefix = "${module.ecs_cluster_label.id}-"
  vpc_id      = var.vpc_id

  lifecycle {
    create_before_destroy = true
  }

  tags = module.ecs_cluster_label.tags
}
