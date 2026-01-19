# Entrypoint for the ecs-service module.

resource "aws_ecs_service" "this" {
  name                               = module.ecs_service_label.id
  cluster                            = var.cluster
  deployment_minimum_healthy_percent = var.min_healthy_percent
  deployment_maximum_percent         = var.max_percent
  desired_count                      = var.desired_count
  force_new_deployment               = var.force_new_deployment
  health_check_grace_period_seconds  = var.health_check_grace_period
  launch_type                        = var.launch_type
  scheduling_strategy                = var.scheduling_strategy
  task_definition                    = var.task_definition

  deployment_circuit_breaker {
    enable   = var.deployment_circuit_breaker.enable
    rollback = var.deployment_circuit_breaker.rollback
  }

  load_balancer {
    container_name   = var.proxy_name
    container_port   = var.proxy_port
    target_group_arn = var.alb_target_group_arn
  }

  network_configuration {
    assign_public_ip = var.assign_public_ip
    security_groups  = var.security_groups
    subnets          = var.subnets
  }

  # Ignore desired_count as it is subject to automatic modification via the
  # auto scaling policies and any updates could result in ECS erreoneously
  # force killing excess containers that might still be in use.
  # https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/ecs_service.html#ignoring-changes-to-desired-count
  lifecycle {
    ignore_changes = [
      desired_count,
      task_definition,
    ]
  }

  tags = module.ecs_service_label.tags
}

locals {
  # https://docs.aws.amazon.com/autoscaling/application/APIReference/API_RegisterScalableTarget.html#API_RegisterScalableTarget_RequestSyntax
  resource_id = "service/${var.cluster_name}/${aws_ecs_service.this.name}"
}

resource "aws_appautoscaling_target" "ecs_target" {
  resource_id        = local.resource_id
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
  min_capacity       = var.min_capacity
  max_capacity       = var.max_capacity

  tags = module.ecs_service_autoscaling_target_label.tags
}

resource "aws_appautoscaling_policy" "ecs_policy_cpu" {
  name               = module.ecs_service_autoscaling_cpu_label.id
  policy_type        = var.scaling_policy_type
  resource_id        = aws_appautoscaling_target.ecs_target.resource_id
  scalable_dimension = aws_appautoscaling_target.ecs_target.scalable_dimension
  service_namespace  = aws_appautoscaling_target.ecs_target.service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }

    target_value       = var.cpu_target_value
    scale_in_cooldown  = var.cpu_scale_in_cooldown
    scale_out_cooldown = var.cpu_scale_out_cooldown
  }
}

resource "aws_appautoscaling_policy" "ecs_policy_memory" {
  name               = module.ecs_service_autoscaling_memory_label.id
  policy_type        = var.scaling_policy_type
  resource_id        = aws_appautoscaling_target.ecs_target.resource_id
  scalable_dimension = aws_appautoscaling_target.ecs_target.scalable_dimension
  service_namespace  = aws_appautoscaling_target.ecs_target.service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageMemoryUtilization"
    }

    target_value       = var.memory_target_value
    scale_in_cooldown  = var.memory_scale_in_cooldown
    scale_out_cooldown = var.memory_scale_out_cooldown
  }
}
