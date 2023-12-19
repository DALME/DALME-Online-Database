terraform {
  source = "../../../modules//ecs/"

  after_hook "init_lock_providers" {
    commands = ["init"]
    execute = [
      "terraform",
      "providers",
      "lock",
      "-platform=linux_amd64",
      "-platform=darwin_amd64",
      "-platform=darwin_arm64",
    ]
    run_on_error = false
  }

  after_hook "init_copy_back_lockfile" {
    commands     = ["init"]
    execute      = ["cp", ".terraform.lock.hcl", "${get_terragrunt_dir()}"]
    run_on_error = false
  }
}

locals {
  env             = read_terragrunt_config(find_in_parent_folders("env.hcl"))
  region_env      = read_terragrunt_config(find_in_parent_folders("region.hcl"))
  admins          = local.env.locals.admins
  aws_account     = local.env.locals.aws_account
  aws_region      = local.region_env.locals.aws_region
  environment     = local.env.locals.environment
  oauth_client_id = local.env.locals.oauth_client_id
  ports           = local.env.locals.ports
  service         = local.env.locals.service
  tenant_domains  = local.env.locals.tenant_domains
  allowed_hosts   = local.tenant_domains
  scheduled_tasks = {
    cleartokens = {
      assign_public_ip    = true,
      is_enabled          = true,
      schedule_expression = "cron(0 2 * * ? *)", # Everyday at 2am.
    },
    publish = {
      assign_public_ip    = true,
      is_enabled          = true,
      schedule_expression = "cron(0 2 * * ? *)", # Everyday at 2am.
    },
  }
}

dependency "alb" {
  config_path                             = "../alb/"
  skip_outputs                            = tobool(get_env("TF_SKIP_OUTPUTS", "false"))
  mock_outputs_allowed_terraform_commands = ["destroy", "init", "plan", "validate"]
  mock_outputs_merge_strategy_with_state  = "shallow"
  mock_outputs = {
    target_group_arn = "arn:aws:elasticloadbalancing:us-east-1:000000000000:targetgroup/some-target/0000000000000000",
  }
}

dependency "cloudfront" {
  config_path                             = "../cloudfront/"
  skip_outputs                            = tobool(get_env("TF_SKIP_OUTPUTS", "false"))
  mock_outputs_allowed_terraform_commands = ["destroy", "init", "plan", "validate"]
  mock_outputs_merge_strategy_with_state  = "shallow"
  mock_outputs = {
    arn                = "arn:aws:cloudfront::000000000000:distribution/ABCDEFGHIJKLMN",
    domain             = "example.com",
    staticfiles_arn    = "arn:aws:s3:::another-bucket",
    staticfiles_bucket = "some-bucket-name",
  }
}

dependency "ecr" {
  config_path                             = "../ecr/"
  skip_outputs                            = tobool(get_env("TF_SKIP_OUTPUTS", "false"))
  mock_outputs_allowed_terraform_commands = ["destroy", "init", "plan", "validate"]
  mock_outputs_merge_strategy_with_state  = "shallow"
  mock_outputs = {
    repository_arns = [
      "arn:aws:ecr:us-east-1:012345678910:repository-namespace/repository-name",
    ],
  }
}

dependency "opensearch" {
  config_path                             = "../opensearch/"
  skip_outputs                            = tobool(get_env("TF_SKIP_OUTPUTS", "false"))
  mock_outputs_allowed_terraform_commands = ["destroy", "init", "plan", "validate"]
  mock_outputs_merge_strategy_with_state  = "shallow"
  mock_outputs = {
    endpoint         = "vpc-some-opensearch-domain-abcdefghijklmnopqrstuvwxyz.us-east-1.es.amazonaws.com"
    master_user_name = "some-user-name"
  }
}

dependency "postgres" {
  config_path                             = "../postgres/"
  skip_outputs                            = tobool(get_env("TF_SKIP_OUTPUTS", "false"))
  mock_outputs_allowed_terraform_commands = ["destroy", "init", "plan", "validate"]
  mock_outputs_merge_strategy_with_state  = "shallow"
  mock_outputs = {
    address                = "some address",
    name                   = "some name",
    username               = "some username",
    master_user_secret_arn = "arn:aws:secretsmanager:us-east-1:00000000:some:secret-abcdefg",
  }
}

dependency "secrets" {
  config_path                             = "../secrets/"
  skip_outputs                            = tobool(get_env("TF_SKIP_OUTPUTS", "false"))
  mock_outputs_allowed_terraform_commands = ["destroy", "init", "plan", "validate"]
  mock_outputs_merge_strategy_with_state  = "shallow"
  mock_outputs = {
    kms_key_arn = "arn:aws:kms:us-east-1:000000000000:key/00000000-0000-0000-0000-000000000000",
    secrets = {
      SOME_SECRET = {
        name      = "some-prefix-SOME-SECRET",
        valueFrom = "arn:aws:secretsmanager:us-east-1:00000000:some:secret-hijklmn",
      }
    },
    secrets_arns = [
      "arn:aws:secretsmanager:us-east-1:00000000:some:secret-opqrstu",
      "arn:aws:secretsmanager:us-east-1:00000000:some:secret-vwxyzab",
    ],
  }
}

dependency "vpc" {
  config_path                             = "../vpc/"
  skip_outputs                            = tobool(get_env("TF_SKIP_OUTPUTS", "false"))
  mock_outputs_allowed_terraform_commands = ["destroy", "init", "plan", "validate"]
  mock_outputs_merge_strategy_with_state  = "shallow"
  mock_outputs = {
    security_groups = {
      ecs = "sg-00000000000000000",
    },
    subnets = {
      private = [
        "subnet-00000000000000000",
        "subnet-00000000000000001",
      ],
    }
  }
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
  admins                       = local.admins
  alb_target_group_arn         = dependency.alb.outputs.target_group_arn
  allowed_hosts                = local.allowed_hosts
  aws_account                  = local.aws_account
  aws_region                   = local.aws_region
  capacity_provider            = "FARGATE_SPOT"
  cloudfront_arn               = dependency.cloudfront.outputs.arn
  cloudfront_domain            = dependency.cloudfront.outputs.domain
  cpu_scale_in_cooldown        = 300
  cpu_scale_out_cooldown       = 300
  cpu_target_value             = 60
  db_host                      = dependency.postgres.outputs.address
  db_name                      = dependency.postgres.outputs.name
  ecs_security_groups          = [dependency.vpc.outputs.security_groups.ecs]
  environment                  = local.environment
  fargate_cpu                  = 256
  fargate_memory               = 1024
  gunicorn_config              = "dalme.gunicorn"
  health_check_grace_period    = 60
  image                        = local.service
  kms_key_arn                  = dependency.secrets.outputs.kms_key_arn
  log_retention_in_days        = 7
  log_level                    = "INFO"
  max_capacity                 = 4
  max_percent                  = 200
  memory_scale_in_cooldown     = 300
  memory_scale_out_cooldown    = 300
  memory_target_value          = 80
  min_capacity                 = 1
  min_healthy_percent          = 100
  oauth_client_id              = local.oauth_client_id
  opensearch_endpoint          = dependency.opensearch.outputs.endpoint
  opensearch_username          = dependency.opensearch.outputs.master_user_name
  postgres_password_secret_arn = dependency.postgres.outputs.master_user_secret_arn
  proxy_port                   = local.ports.proxy
  registry                     = "${local.aws_account}.dkr.ecr.${local.aws_region}.amazonaws.com"
  repository_arns              = dependency.ecr.outputs.repository_arns
  scaling_policy_type          = "TargetTrackingScaling"
  scheduled_tasks              = local.scheduled_tasks
  secrets                      = dependency.secrets.outputs.secrets
  secrets_arns                 = dependency.secrets.outputs.secrets_arns
  service                      = local.service
  service_desired_count        = 1
  sfn_backoff_rate             = 1.5
  sfn_heartbeat                = 60
  sfn_max_attempts             = 3
  sfn_retry_interval           = 3
  sfn_timeout                  = 300
  staticfiles_arn              = dependency.cloudfront.outputs.staticfiles_arn
  staticfiles_bucket           = dependency.cloudfront.outputs.staticfiles_bucket
  subnets                      = dependency.vpc.outputs.subnets.private
  task_assign_public_ip        = true
  threads                      = 4
  web_port                     = local.ports.web
  worker                       = "gthread"
  worker_tmp                   = "/dev/shm"
  workers                      = 3
  wsgi                         = "dalme.wsgi:application"
}
