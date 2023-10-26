# Terraform definitions for the ecs module.

terraform {
  required_version = "~> 1.3"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.14.0"
    }
  }
}

locals {
  web_env = [
    { name = "ADMIN_USERNAME", value = "${var.service}-super-${var.environment}" },
    { name = "ALLOWED_HOSTS", value = jsonencode(var.allowed_hosts) },
    { name = "AWS_STORAGE_BUCKET_NAME", value = var.staticfiles_bucket },
    { name = "CLOUDFRONT_DISTRIBUTION", value = var.cloudfront_domain },
    { name = "ELASTICSEARCH_ENDPOINT", value = var.opensearch_endpoint },
    { name = "ELASTICSEARCH_USER", value = var.opensearch_username },
    { name = "ENV", value = var.environment },
    { name = "LOG_LEVEL", value = var.log_level },
    { name = "POSTGRES_DB", value = var.db_name },
    { name = "POSTGRES_HOST", value = var.db_host },
    { name = "TENANT_DOMAINS", value = jsonencode(var.tenant_domains) },
  ]
  web_image   = "${var.registry}/${var.image}.web:${var.environment}"
  protocol    = "tcp"
  proxy_image = "${var.registry}/${var.image}.proxy:${var.environment}"
  proxy_name  = "nginx"
  secrets = [
    var.secrets["ADMIN_PASSWORD"],
    var.secrets["DJANGO_SECRET_KEY"],
    {
      # Just an easy way to rename this for the container.
      name      = "ELASTICSEARCH_PASSWORD",
      valueFrom = var.secrets["OPENSEARCH_PASSWORD"].valueFrom
    },
    # Note that when rds manages its own password it comes as a user/password pair.
    { name = "POSTGRES_USER", valueFrom = "${var.postgres_password_secret_arn}:username::" },
    { name = "POSTGRES_PASSWORD", valueFrom = "${var.postgres_password_secret_arn}:password::" },
  ]
}

resource "aws_ecs_cluster" "main" {
  name = "${var.service}-ecs-cluster-${var.environment}"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }

  tags = {
    Name = "${var.service}-ecs-cluster-${var.environment}"
  }
}

resource "aws_ecs_cluster_capacity_providers" "main" {
  cluster_name = aws_ecs_cluster.main.name

  capacity_providers = [var.capacity_provider]

  default_capacity_provider_strategy {
    base              = 1
    weight            = 100
    capacity_provider = var.capacity_provider
  }
}

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
      name        = "collectstatic_schemas"
      image       = local.web_image
      environment = local.web_env
      secrets     = local.secrets
      essential   = false
      command = [
        "python3",
        "manage.py",
        "all_tenants_command",
        "collectstatic",
        "--noinput",
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
      name        = "collectstatic"
      image       = local.web_image
      environment = local.web_env
      secrets     = local.secrets
      essential   = false
      command     = ["python3", "manage.py", "collectstatic", "--noinput"]
      dependsOn = [
        { containerName = var.service, condition = "HEALTHY" },
        { containerName = "collectstatic_schemas", condition = "SUCCESS" },
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

resource "aws_ecs_service" "main" {
  name                               = "${var.service}-ecs-service-${var.environment}"
  cluster                            = aws_ecs_cluster.main.arn
  deployment_minimum_healthy_percent = var.min_healthy_percent
  deployment_maximum_percent         = var.max_percent
  desired_count                      = var.service_desired_count
  force_new_deployment               = false
  health_check_grace_period_seconds  = var.health_check_grace_period
  launch_type                        = "FARGATE"
  scheduling_strategy                = "REPLICA"
  task_definition                    = aws_ecs_task_definition.main.arn

  network_configuration {
    assign_public_ip = true
    security_groups  = var.ecs_security_groups
    subnets          = var.subnets
  }

  load_balancer {
    container_name   = local.proxy_name
    container_port   = var.proxy_port
    target_group_arn = var.alb_target_group_arn
  }

  # Ignore desired_count as it is subject to automatic modification via the
  # auto scaling policies and any updates could result in ECS erreoneously
  # force killing excess containers that might still be in use.
  # https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/ecs_service.html#ignoring-changes-to-desired-count
  lifecycle {
    ignore_changes = [task_definition, desired_count]
  }

  tags = {
    Name = "${var.service}-ecs-service-${var.environment}"
  }
}

resource "aws_cloudwatch_log_group" "web_log_group" {
  name              = "${var.service}/ecs/web/${var.environment}/logs"
  kms_key_id        = var.kms_key_arn
  retention_in_days = var.log_retention_in_days

  tags = {
    Name = "${var.service}/ecs/web/${var.environment}/logs"
  }
}

resource "aws_cloudwatch_log_stream" "web_log_stream" {
  name           = "${var.service}-ecs-web-log-stream-${var.environment}"
  log_group_name = aws_cloudwatch_log_group.web_log_group.name
}

resource "aws_cloudwatch_log_group" "proxy_log_group" {
  name              = "${var.service}/ecs/proxy/${var.environment}/logs"
  kms_key_id        = var.kms_key_arn
  retention_in_days = var.log_retention_in_days

  tags = {
    Name = "${var.service}/ecs/proxy/${var.environment}/logs"
  }
}

resource "aws_cloudwatch_log_stream" "proxy_log_stream" {
  name           = "${var.service}-ecs-proxy-log-stream-${var.environment}"
  log_group_name = aws_cloudwatch_log_group.proxy_log_group.name
}
