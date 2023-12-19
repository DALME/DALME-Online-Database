# Task definitions for the ecs module.

resource "aws_ecs_task_definition" "main" {
  family                   = "${var.service}-task-definition-web-${var.environment}"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.fargate_cpu
  memory                   = var.fargate_memory
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_role.arn

  container_definitions = jsonencode([
    {
      name      = local.proxy_name
      image     = local.proxy_image
      essential = true
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.proxy_log_group.name
          awslogs-region        = var.aws_region
          awslogs-stream-prefix = "ecs"
        }
      }
      portMappings = [
        {
          containerPort = var.proxy_port
          protocol      = local.protocol
        }
      ]
    },
    {
      name        = var.service
      image       = local.web_image
      environment = local.web_env
      secrets     = local.secrets
      essential   = true
      command = [
        "gunicorn",
        "--log-file=-",
        "--bind=:${var.web_port}",
        "--threads=${var.threads}",
        "--workers=${var.workers}",
        "--worker-class=${var.worker}",
        "--worker-tmp-dir=${var.worker_tmp}",
        "--config=python:${var.gunicorn_config}",
        var.wsgi,
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.web_log_group.name
          awslogs-region        = var.aws_region
          awslogs-stream-prefix = "ecs"
        }
      }
      portMappings = [
        {
          containerPort = var.web_port
          hostPort      = var.web_port
          protocol      = local.protocol
        }
      ]
      healthCheck = {
        command = [
          "CMD-SHELL", "curl -f http://localhost:${var.web_port}/api/healthcheck/ || exit 1"
        ]
      }
    },
    {
      name        = "migrate"
      image       = local.web_image
      environment = local.web_env
      secrets     = local.secrets
      essential   = false
      command     = ["python3", "manage.py", "migrate_schemas"]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.web_log_group.name
          awslogs-region        = var.aws_region
          awslogs-stream-prefix = "ecs"
        }
      }
    },
    {
      name        = "createcachetable"
      image       = local.web_image
      environment = local.web_env
      secrets     = local.secrets
      essential   = false
      command     = ["python3", "manage.py", "custom_createcachetable"]
      dependsOn = [
        { containerName = var.service, condition = "HEALTHY" },
        { containerName = "migrate", condition = "SUCCESS" },
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.web_log_group.name
          awslogs-region        = var.aws_region
          awslogs-stream-prefix = "ecs"
        }
      }
    },
    {
      name        = "ensure_tenants"
      image       = local.web_image
      environment = local.web_env
      secrets     = local.secrets
      essential   = false
      command     = ["python3", "manage.py", "ensure_tenants"]
      dependsOn = [
        { containerName = var.service, condition = "HEALTHY" },
        { containerName = "createcachetable", condition = "SUCCESS" },
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.web_log_group.name
          awslogs-region        = var.aws_region
          awslogs-stream-prefix = "ecs"
        }
      }
    },
    {
      name        = "collectstatic"
      image       = local.web_image
      environment = local.web_env
      secrets     = local.secrets
      essential   = false
      command = [
        "python3",
        "manage.py",
        "collectstatic_tenants",
      ]
      dependsOn = [
        { containerName = var.service, condition = "HEALTHY" },
        { containerName = "ensure_tenants", condition = "SUCCESS" },
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.web_log_group.name
          awslogs-region        = var.aws_region
          awslogs-stream-prefix = "ecs"
        }
      }
    },
    {
      name        = "ensure_oauth"
      image       = local.web_image
      environment = local.web_env
      secrets     = local.secrets
      essential   = false
      command     = ["python3", "manage.py", "ensure_oauth"]
      dependsOn = [
        { containerName = var.service, condition = "HEALTHY" },
        { containerName = "createcachetable", condition = "SUCCESS" },
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.web_log_group.name
          awslogs-region        = var.aws_region
          awslogs-stream-prefix = "ecs"
        }
      }
    },
    {
      name        = "ensure_superuser"
      image       = local.web_image
      environment = local.web_env
      secrets     = local.secrets
      essential   = false
      command     = ["python3", "manage.py", "ensure_superuser"]
      dependsOn = [
        { containerName = var.service, condition = "HEALTHY" },
        { containerName = "createcachetable", condition = "SUCCESS" },
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.web_log_group.name
          awslogs-region        = var.aws_region
          awslogs-stream-prefix = "ecs"
        }
      }
    },
  ])

  tags = {
    Name = "${var.service}-ecs-task-definition-web-${var.environment}"
  }
}
