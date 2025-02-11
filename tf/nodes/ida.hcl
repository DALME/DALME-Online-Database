# Inject the ida module.

terraform {
  source = "../../../..//modules/services/ida/"
}

locals {
  env         = read_terragrunt_config(find_in_parent_folders("environment.hcl"))
  admins      = local.env.locals.admins
  domain      = local.env.locals.domain
  environment = local.env.locals.environment
  # https://registry.terraform.io/providers/hashicorp/random/latest/docs#resource-keepers
  keepers = {
    admin_user_version          = 1,
    django_secret_key_version   = 1,
    oauth_client_secret_version = 1,
  }
  namespace                          = local.env.locals.namespace
  oauth_client_id                    = local.env.locals.oauth_client_id
  opensearch_master_user_secret_name = local.env.locals.opensearch_master_user_secret_name
  ports                              = local.env.locals.ports
  postgres_version                   = local.env.locals.postgres_version
  # https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/publishEvents.html#CronExpressions
  scheduled_tasks = {
    cleartokens = {
      assign_public_ip    = true,
      schedule_expression = "cron(0 2 * * ? *)", # Everyday at 2am.
      state               = "ENABLED",
    },
    publish = {
      assign_public_ip    = true,
      schedule_expression = "cron(0 2 * * ? *)", # Everyday at 2am.
      state               = "ENABLED",
    },
  }
  tenant_domains   = local.env.locals.tenant_domains
  unmanaged_suffix = local.env.locals.unmanaged_suffix
}

# Valid Fargate CPU/memory combinations
# -------------------------------------
# CPU value       Memory value (MiB)
# 256 (.25 vCPU)  512 (0.5GB), 1024 (1GB), 2048 (2GB)
# 512 (.5 vCPU)   1024 (1GB), 2048 (2GB), 3072 (3GB), 4096 (4GB)
# 1024 (1 vCPU)   2048 (2GB), 3072 (3GB), 4096 (4GB), 5120 (5GB), 6144 (6GB), 7168 (7GB), 8192 (8GB)
# 2048 (2 vCPU)   Between 4096 (4GB) and 16384 (16GB) in increments of 1024 (1GB)
# 4096 (4 vCPU)   Between 8192 (8GB) and 30720 (30GB) in increments of 1024 (1GB)

inputs = {
  admins                             = local.admins
  allowed_hosts                      = local.tenant_domains
  app_port                           = local.ports.app
  assign_public_ip                   = true
  cpu_scale_in_cooldown              = 300
  cpu_scale_out_cooldown             = 300
  cpu_target_value                   = 60
  domain                             = local.domain
  fargate_cpu                        = 256
  fargate_memory                     = 1024
  force_delete                       = contains(["development", "staging"], local.environment)
  force_new_deployment               = false
  gunicorn_config                    = "app.gunicorn"
  health_check_grace_period          = 60
  images                             = ["app", "proxy"]
  keepers                            = local.keepers
  launch_type                        = "FARGATE"
  log_level                          = "INFO"
  log_retention_in_days              = 7
  max_capacity                       = local.environment == "staging" ? 1 : 4
  max_percent                        = 200
  memory_scale_in_cooldown           = 300
  memory_scale_out_cooldown          = 300
  memory_target_value                = 80
  min_capacity                       = 1
  min_healthy_percent                = 100
  oauth_client_id                    = local.oauth_client_id
  opensearch_master_user_secret_name = local.opensearch_master_user_secret_name
  postgres_version                   = local.postgres_version
  proxy_port                         = local.ports.proxy
  recovery_window                    = local.environment == "production" ? 7 : 0
  retain_n                           = 10
  scaling_policy_type                = "TargetTrackingScaling"
  scheduled_tasks                    = local.scheduled_tasks
  scheduling_strategy                = "REPLICA"
  service_desired_count              = 1
  sfn_backoff_rate                   = 1.5
  sfn_heartbeat                      = 60
  sfn_max_attempts                   = 3
  sfn_retry_interval                 = 3
  sfn_timeout                        = 300
  task_assign_public_ip              = true
  tenant_domains                     = local.tenant_domains
  threads                            = 4
  unmanaged_suffix                   = local.unmanaged_suffix
  worker                             = "gthread"
  worker_tmp                         = "/dev/shm"
  workers                            = 3
  wsgi                               = "app.wsgi:application"
}
