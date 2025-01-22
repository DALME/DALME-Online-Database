# Entrypoint for the ida module.

# Repositories
module "ecr" {
  for_each = toset(var.images)
  source   = "../..//_reusable/ecr/"

  environment  = var.environment
  force_delete = var.force_delete
  image        = each.key
  namespace    = var.namespace
  kms_key_arn  = data.aws_kms_alias.global.target_key_arn
  retain_n     = var.retain_n
}

# Secrets
locals {
  postgres_master_user_secret_arn = data.aws_db_instance.postgres.master_user_secret[0].secret_arn
  # These are secrets that we generate here and manage entirely through
  # Terraform, as opposed to those secrets marked 'UNMANAGED' that require some
  # manual intervention in order to get them populated and ready for use.
  secret_data = {
    "ADMIN-USER" = {
      description            = "Credentials for the Django superuser."
      keepers                = { version = var.keepers.admin_user_version }
      username               = "${var.namespace}-${var.environment}-superuser"
      username_password_pair = true
    },
    "DJANGO-SECRET-KEY" = {
      description            = "Random string required by Django to sign secure data."
      keepers                = { version = var.keepers.django_secret_key_version }
      username_password_pair = false
    },
    "OAUTH-CLIENT-SECRET" = {
      description            = "Random string required by OAuth2 logic to sign secure data."
      keepers                = { version = var.keepers.oauth_client_secret_version }
      username_password_pair = false
    },
  }
}

module "secret" {
  source = "../..//_reusable/secret/"

  for_each = local.secret_data

  name                   = each.key
  description            = each.value.description
  environment            = var.environment
  keepers                = each.value.keepers
  kms_key_arn            = data.aws_kms_alias.global.target_key_arn
  namespace              = var.namespace
  recovery_window        = var.recovery_window
  username_password_pair = each.value.username_password_pair
  username               = try(each.value.username, null)
}

# Logs
resource "aws_cloudwatch_log_group" "web_log_group" {
  name              = module.ida_log_group_web_label.id
  kms_key_id        = data.aws_kms_alias.global.target_key_arn
  retention_in_days = var.log_retention_in_days

  tags = module.ida_log_group_web_label.tags
}

resource "aws_cloudwatch_log_stream" "web_log_stream" {
  name           = module.ida_log_stream_web_label.id
  log_group_name = aws_cloudwatch_log_group.web_log_group.name
}

resource "aws_cloudwatch_log_group" "proxy_log_group" {
  name              = module.ida_log_group_proxy_label.id
  kms_key_id        = data.aws_kms_alias.global.target_key_arn
  retention_in_days = var.log_retention_in_days

  tags = module.ida_log_group_proxy_label.tags
}

resource "aws_cloudwatch_log_stream" "proxy_log_stream" {
  name           = module.ida_log_stream_proxy_label.id
  log_group_name = aws_cloudwatch_log_group.proxy_log_group.name
}

# ECS task definition.
locals {
  registry = "${var.aws_account}.dkr.ecr.${var.aws_region}.amazonaws.com"
  tag      = var.environment == "production" ? "latest" : "staging"
}

locals {
  images = {
    proxy = "${local.registry}/${var.namespace}.proxy:${local.tag}",
    app   = "${local.registry}/${var.namespace}.app:${local.tag}",
  }
  protocol   = "tcp"
  proxy_name = "nginx"
  app_env = [
    { name = "ALLOWED_HOSTS", value = jsonencode(var.allowed_hosts) },
    { name = "AWS_STORAGE_BUCKET_NAME", value = data.aws_s3_bucket.staticfiles.id },
    { name = "CLOUDFRONT_DISTRIBUTION", value = data.external.cloudfront.result.domain },
    { name = "DJANGO_CONFIGURATION", value = var.environment == "production" ? "Production" : "Staging" },
    { name = "DJANGO_SETTINGS_MODULE", value = "app.settings" },
    { name = "DOMAIN", value = var.domain },
    { name = "ELASTICSEARCH_ENDPOINT", value = data.aws_opensearch_domain.this.endpoint },
    { name = "ENV", value = var.environment },
    { name = "LOG_LEVEL", value = var.log_level },
    { name = "OAUTH_CLIENT_ID", value = var.oauth_client_id },
    { name = "POSTGRES_DB", value = data.aws_db_instance.postgres.db_name },
    { name = "POSTGRES_HOST", value = data.aws_db_instance.postgres.address },
    { name = "TENANT_DOMAINS", value = jsonencode(var.tenant_domains) },
  ]
  app_secrets = [
    { name = "ADMIN_USERNAME", valueFrom = "${module.secret["ADMIN-USER"].arn}:username::" },
    { name = "ADMIN_PASSWORD", valueFrom = "${module.secret["ADMIN-USER"].arn}:password::" },
    { name = "DAM_API_USER", valueFrom = "${data.aws_secretsmanager_secret_version.dam.arn}:api_user::" },
    { name = "DAM_API_KEY", valueFrom = "${data.aws_secretsmanager_secret_version.dam.arn}:api_key::" },
    { name = "DAM_DB_NAME", valueFrom = "${data.aws_secretsmanager_secret_version.dam.arn}:db_name::" },
    { name = "DAM_DB_USER", valueFrom = "${data.aws_secretsmanager_secret_version.dam.arn}:db_user::" },
    { name = "DAM_DB_PASSWORD", valueFrom = "${data.aws_secretsmanager_secret_version.dam.arn}:db_password::" },
    { name = "DAM_DB_HOST", valueFrom = "${data.aws_secretsmanager_secret_version.dam.arn}:db_host::" },
    { name = "DAM_DB_PORT", valueFrom = "${data.aws_secretsmanager_secret_version.dam.arn}:db_port::" },
    { name = "DJANGO_SECRET_KEY", valueFrom = module.secret["DJANGO-SECRET-KEY"].arn },
    { name = "ELASTICSEARCH_USER", valueFrom = "${data.aws_secretsmanager_secret_version.opensearch_master_user.arn}:username::" },
    { name = "ELASTICSEARCH_PASSWORD", valueFrom = "${data.aws_secretsmanager_secret_version.opensearch_master_user.arn}:password::" },
    { name = "OAUTH_CLIENT_SECRET", valueFrom = module.secret["OAUTH-CLIENT-SECRET"].arn },
    { name = "OIDC_RSA_PRIVATE_KEY", valueFrom = "${data.aws_secretsmanager_secret_version.oidc_rsa_key.arn}:private::" },
    { name = "POSTGRES_USER", valueFrom = "${local.postgres_master_user_secret_arn}:username::" },
    { name = "POSTGRES_PASSWORD", valueFrom = "${local.postgres_master_user_secret_arn}:password::" },
    { name = "ZOTERO_API_KEY", valueFrom = "${data.aws_secretsmanager_secret_version.zotero.arn}:api_key::" },
    { name = "ZOTERO_API_KEY_GP", valueFrom = "${data.aws_secretsmanager_secret_version.zotero.arn}:api_key_gp::" },
    { name = "ZOTERO_LIBRARY_ID", valueFrom = "${data.aws_secretsmanager_secret_version.zotero.arn}:library_id::" },
    { name = "ZOTERO_LIBRARY_ID_GP", valueFrom = "${data.aws_secretsmanager_secret_version.zotero.arn}:library_id_gp::" },
  ]
}

resource "aws_ecs_task_definition" "this" {
  family                   = module.ida_ecs_task_definition_label.id
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.fargate_cpu
  memory                   = var.fargate_memory
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_role.arn

  container_definitions = jsonencode(
    [
      {
        cpu         = 0
        environment = []
        essential   = true
        image       = local.images.proxy
        logConfiguration = {
          logDriver = "awslogs"
          options = {
            awslogs-group         = aws_cloudwatch_log_group.proxy_log_group.name
            awslogs-region        = var.aws_region
            awslogs-stream-prefix = "ecs"
          }
        }
        mountPoints = []
        name        = local.proxy_name
        portMappings = [
          {
            hostPort      = var.proxy_port
            containerPort = var.proxy_port
            protocol      = local.protocol
          }
        ]
        systemControls = []
        volumesFrom    = []
      },
      {
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
        cpu         = 0
        environment = local.app_env
        essential   = true
        healthCheck = {
          command = [
            "CMD-SHELL", "curl -f http://localhost:${var.web_port}/api/healthcheck/ || exit 1"
          ]
          interval = 30
          retries  = 3
          timeout  = 5
        }
        image = local.images.app
        logConfiguration = {
          logDriver = "awslogs"
          options = {
            awslogs-group         = aws_cloudwatch_log_group.web_log_group.name
            awslogs-region        = var.aws_region
            awslogs-stream-prefix = "ecs"
          }
        }
        mountPoints = []
        name        = var.namespace
        portMappings = [
          {
            containerPort = var.web_port
            hostPort      = var.web_port
            protocol      = local.protocol
          }
        ]
        secrets        = local.app_secrets
        systemControls = []
        volumesFrom    = []
      },
      {
        command     = ["python3", "manage.py", "migrate_schemas"]
        cpu         = 0
        environment = local.app_env
        essential   = false
        image       = local.images.app
        logConfiguration = {
          logDriver = "awslogs"
          options = {
            awslogs-group         = aws_cloudwatch_log_group.web_log_group.name
            awslogs-region        = var.aws_region
            awslogs-stream-prefix = "ecs"
          }
        }
        mountPoints    = []
        name           = "migrate"
        portMappings   = []
        secrets        = local.app_secrets
        systemControls = []
        volumesFrom    = []
      },
      {
        command = ["python3", "manage.py", "collectstatic_tenants"]
        cpu     = 0
        dependsOn = [
          { containerName = var.namespace, condition = "HEALTHY" },
        ]
        environment = local.app_env
        essential   = false
        image       = local.images.app
        logConfiguration = {
          logDriver = "awslogs"
          options = {
            awslogs-group         = aws_cloudwatch_log_group.web_log_group.name
            awslogs-region        = var.aws_region
            awslogs-stream-prefix = "ecs"
          }
        }
        mountPoints    = []
        name           = "collectstatic"
        portMappings   = []
        secrets        = local.app_secrets
        systemControls = []
        volumesFrom    = []
      },
      {
        command = ["python3", "manage.py", "ensure_oauth"]
        cpu     = 0
        dependsOn = [
          { containerName = var.namespace, condition = "HEALTHY" },
        ]
        environment = local.app_env
        essential   = false
        image       = local.images.app
        logConfiguration = {
          logDriver = "awslogs"
          options = {
            awslogs-group         = aws_cloudwatch_log_group.web_log_group.name
            awslogs-region        = var.aws_region
            awslogs-stream-prefix = "ecs"
          }
        }
        mountPoints    = []
        name           = "ensure_oauth"
        portMappings   = []
        secrets        = local.app_secrets
        systemControls = []
        volumesFrom    = []
      },
      {
        command = ["python3", "manage.py", "ensure_tenants"]
        cpu     = 0
        dependsOn = [
          { containerName = var.namespace, condition = "HEALTHY" },
        ]
        environment = local.app_env
        essential   = false
        image       = local.images.app
        logConfiguration = {
          logDriver = "awslogs"
          options = {
            awslogs-group         = aws_cloudwatch_log_group.web_log_group.name
            awslogs-region        = var.aws_region
            awslogs-stream-prefix = "ecs"
          }
        }
        mountPoints    = []
        name           = "ensure_tenants"
        portMappings   = []
        secrets        = local.app_secrets
        systemControls = []
        volumesFrom    = []
      },
      {
        command = ["python3", "manage.py", "ensure_superuser"]
        cpu     = 0
        dependsOn = [
          { containerName = var.namespace, condition = "HEALTHY" }
        ]
        environment = local.app_env
        essential   = false
        image       = local.images.app
        logConfiguration = {
          logDriver = "awslogs"
          options = {
            awslogs-group         = aws_cloudwatch_log_group.web_log_group.name
            awslogs-region        = var.aws_region
            awslogs-stream-prefix = "ecs"
          }
        }
        mountPoints    = []
        name           = "ensure_superuser"
        portMappings   = []
        secrets        = local.app_secrets
        systemControls = []
        volumesFrom    = []
      },
    ]
  )

  tags = module.ida_ecs_task_definition_label.tags
}

# ECS service
module "ecs_service" {
  source = "../..//_reusable/ecs-service/"

  alb_target_group_arn      = data.aws_lb_target_group.this.arn
  assign_public_ip          = var.assign_public_ip
  cluster                   = data.aws_ecs_cluster.this.arn
  cluster_name              = data.aws_ecs_cluster.this.cluster_name
  cpu_scale_in_cooldown     = var.cpu_scale_in_cooldown
  cpu_scale_out_cooldown    = var.cpu_scale_out_cooldown
  cpu_target_value          = var.cpu_target_value
  desired_count             = var.service_desired_count
  environment               = var.environment
  force_new_deployment      = var.force_new_deployment
  health_check_grace_period = var.health_check_grace_period
  launch_type               = var.launch_type
  max_capacity              = var.max_capacity
  max_percent               = var.max_percent
  memory_scale_in_cooldown  = var.memory_scale_in_cooldown
  memory_scale_out_cooldown = var.memory_scale_out_cooldown
  memory_target_value       = var.memory_target_value
  min_capacity              = var.min_capacity
  min_healthy_percent       = var.min_healthy_percent
  namespace                 = var.namespace
  proxy_name                = local.proxy_name
  proxy_port                = var.proxy_port
  scaling_policy_type       = var.scaling_policy_type
  scheduling_strategy       = var.scheduling_strategy
  security_groups           = [data.aws_security_group.ecs.id]
  subnets                   = data.aws_subnets.private.ids
  task_definition           = aws_ecs_task_definition.this.arn
}

# Scheduled tasks/step functions.
resource "aws_sns_topic" "ecs_scheduled_task_failure" {
  name              = module.ida_sns_ecs_scheduled_task_failure_label.id
  kms_master_key_id = data.aws_kms_alias.global.target_key_arn
  delivery_policy = jsonencode({
    "http" : {
      "defaultHealthyRetryPolicy" : {
        "minDelayTarget" : 20,
        "maxDelayTarget" : 20,
        "numRetries" : 3,
        "numMaxDelayRetries" : 0,
        "numNoDelayRetries" : 0,
        "numMinDelayRetries" : 0,
        "backoffFunction" : "linear"
      },
      "disableSubscriptionOverrides" : false,
      "defaultThrottlePolicy" : {
        "maxReceivesPerSecond" : 1
      }
    }
  })

  tags = module.ida_sns_ecs_scheduled_task_failure_label.tags
}

resource "aws_sns_topic_subscription" "ecs_scheduled_task_failure" {
  count     = length(var.admins)
  topic_arn = aws_sns_topic.ecs_scheduled_task_failure.arn
  protocol  = "email"
  endpoint  = var.admins[count.index]
}

# Clear OAuth tokens scheduled task.
resource "aws_ecs_task_definition" "cleartokens" {
  family                   = module.ida_sfn_ecs_scheduled_task_cleartokens_label.id
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.fargate_cpu
  memory                   = var.fargate_memory
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_role.arn

  container_definitions = jsonencode([
    {
      command     = ["python3", "manage.py", "cleartokens"]
      cpu         = 0
      environment = local.app_env
      essential   = true
      image       = local.images.app
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.web_log_group.name
          awslogs-region        = var.aws_region
          awslogs-stream-prefix = "ecs-scheduled-task"
        }
      }
      mountPoints    = []
      name           = "cleartokens"
      portMappings   = []
      secrets        = local.app_secrets
      systemControls = []
      volumesFrom    = []
    },
  ])

  tags = module.ida_sfn_ecs_scheduled_task_cleartokens_label.tags
}

module "sfn_cleartokens" {
  source = "../..//_reusable/sfn-ecs-scheduled-task/"

  assign_public_ip            = var.scheduled_tasks.cleartokens.assign_public_ip
  aws_account                 = var.aws_account
  aws_region                  = var.aws_region
  backoff_rate                = var.sfn_backoff_rate
  cluster                     = data.aws_ecs_cluster.this.arn
  container                   = "cleartokens"
  description                 = "Remove expired OAuth refresh tokens."
  ecs_task_definition_arn     = aws_ecs_task_definition.cleartokens.arn
  ecs_task_execution_role_arn = aws_iam_role.ecs_task_execution_role.arn
  ecs_task_role_arn           = aws_iam_role.ecs_task_role.arn
  environment                 = var.environment
  failure_sns_topic           = aws_sns_topic.ecs_scheduled_task_failure.arn
  heartbeat                   = var.sfn_heartbeat
  kms_key_arn                 = data.aws_kms_alias.global.target_key_arn
  launch_type                 = var.launch_type
  max_attempts                = var.sfn_max_attempts
  name                        = "cleartokens"
  namespace                   = var.namespace
  retry_interval              = var.sfn_retry_interval
  schedule_expression         = var.scheduled_tasks.cleartokens.schedule_expression
  security_groups             = [data.aws_security_group.ecs.id]
  state                       = var.scheduled_tasks.cleartokens.state
  subnets                     = data.aws_subnets.private.ids
  timeout                     = var.sfn_timeout
}

# Publish Wagtail pages scheduled task.
resource "aws_ecs_task_definition" "publish" {
  family                   = module.ida_sfn_ecs_scheduled_task_publish_label.id
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.fargate_cpu
  memory                   = var.fargate_memory
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_role.arn

  container_definitions = jsonencode([
    {
      command     = ["python3", "manage.py", "publish_pags"]
      cpu         = 0
      environment = local.app_env
      essential   = true
      image       = local.images.app
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.web_log_group.name
          awslogs-region        = var.aws_region
          awslogs-stream-prefix = "ecs-scheduled-task"
        }
      }
      mountPoints    = []
      name           = "publish"
      portMappings   = []
      secrets        = local.app_secrets
      systemControls = []
      volumesFrom    = []
    },
  ])

  tags = module.ida_sfn_ecs_scheduled_task_publish_label.tags
}

module "sfn_publish" {
  source = "../..//_reusable/sfn-ecs-scheduled-task/"

  assign_public_ip            = var.scheduled_tasks.publish.assign_public_ip
  aws_account                 = var.aws_account
  aws_region                  = var.aws_region
  backoff_rate                = var.sfn_backoff_rate
  cluster                     = data.aws_ecs_cluster.this.arn
  container                   = "publish"
  description                 = "Remove expired OAuth refresh tokens."
  ecs_task_definition_arn     = aws_ecs_task_definition.publish.arn
  ecs_task_execution_role_arn = aws_iam_role.ecs_task_execution_role.arn
  ecs_task_role_arn           = aws_iam_role.ecs_task_role.arn
  environment                 = var.environment
  failure_sns_topic           = aws_sns_topic.ecs_scheduled_task_failure.arn
  heartbeat                   = var.sfn_heartbeat
  kms_key_arn                 = data.aws_kms_alias.global.target_key_arn
  launch_type                 = var.launch_type
  max_attempts                = var.sfn_max_attempts
  name                        = "publish"
  namespace                   = var.namespace
  retry_interval              = var.sfn_retry_interval
  schedule_expression         = var.scheduled_tasks.publish.schedule_expression
  security_groups             = [data.aws_security_group.ecs.id]
  state                       = var.scheduled_tasks.publish.state
  subnets                     = data.aws_subnets.private.ids
  timeout                     = var.sfn_timeout
}
