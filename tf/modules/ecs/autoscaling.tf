# Autoscaling rules for ECS.
locals {
  resource_id = "service/${aws_ecs_cluster.main.name}/${aws_ecs_service.main.name}"
}

resource "aws_appautoscaling_target" "ecs_target" {
  resource_id        = local.resource_id
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
  min_capacity       = var.min_capacity
  max_capacity       = var.max_capacity

  tags = {
    Name = "${var.service}-autoscaling-target-ecs-${var.environment}"
  }
}

resource "aws_appautoscaling_policy" "ecs_policy_cpu" {
  name               = "${var.service}-cpu-autoscaling-${var.environment}"
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
  name               = "${var.service}-memory-autoscaling-${var.environment}"
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
