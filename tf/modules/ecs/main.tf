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
    { name = "OAUTH_CLIENT_ID", value = var.oauth_client_id },
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
    var.secrets["OAUTH_CLIENT_SECRET"],
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
