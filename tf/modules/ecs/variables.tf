# Terraform variables for the ecs module.

variable "admins" {
  description = "Project admin email addresses."
  type        = list(string)
}

variable "alb_target_group_arn" {
  description = "The ARN of the target group for the ALB."
  type        = string
}

variable "allowed_hosts" {
  description = "Permitted domains for requests."
  type        = list(string)
}

variable "aws_account" {
  description = "The AWS account where resources are created."
  type        = number
}

variable "aws_region" {
  description = "The AWS region where resources are created."
  type        = string
}

variable "capacity_provider" {
  description = "Determine where ECS scaling provisioning comes from."
  type        = string
}

variable "cloudfront_arn" {
  description = "ARN for the cloudfront distribution."
  type        = string
}

variable "cloudfront_domain" {
  description = "Pass the cloudfront endpoint for injection in the tasks."
  type        = string
}

variable "cpu_scale_in_cooldown" {
  description = "How long (secs) after a CPU scale-in completes before another can start."
  type        = number
}

variable "cpu_scale_out_cooldown" {
  description = "How long (secs) after a CPU scale-out completes before another can start."
  type        = number
}

variable "cpu_target_value" {
  description = "Target value for the CPU metric."
  type        = number
}

variable "db_host" {
  description = "The host of the db instance."
  type        = string
}

variable "db_name" {
  description = "The name of the db instance."
  type        = string
}

variable "ecs_security_groups" {
  description = "The security groups mapped to the ECS service."
  type        = list(string)
}

variable "environment" {
  description = "Identify the deployment environment."
  type        = string
}

variable "fargate_cpu" {
  description = "Fargate instance CPU units to provision (1 vCPU = 1024 CPU units)."
  type        = number
}

variable "fargate_memory" {
  description = "Fargate instance memory to provision (in MiB)."
  type        = number
}

variable "gunicorn_config" {
  description = "Path to the gunicorn config file."
  type        = string
}

variable "health_check_grace_period" {
  description = "How long to wait before terminating tasks that fail health checks."
  type        = number
}

variable "image" {
  description = "Common container name."
  type        = string
}

variable "kms_key_arn" {
  description = "The project encryption key ARN."
  type        = string
}

variable "log_level" {
  description = "Set the severity of the web logger."
  type        = string
}

variable "log_retention_in_days" {
  description = "How long to keep cloudwatch records."
  type        = number
}

variable "max_capacity" {
  description = "Maximum number for scaling targets."
  type        = number
}

variable "max_percent" {
  description = "The upper limit of running tasks in a service during a deployment."
  type        = number
}

variable "memory_scale_in_cooldown" {
  description = "How long (secs) after a memory scale-in completes before another can start."
  type        = number
}

variable "memory_scale_out_cooldown" {
  description = "How long (secs) after a memory scale-out completes before another can start."
  type        = number
}

variable "memory_target_value" {
  description = "Target value for the memory metric."
  type        = number
}

variable "min_capacity" {
  description = "Minimum number of scaling targets."
  type        = number
}

variable "min_healthy_percent" {
  description = "The lower limit of running tasks that must remain healthy in a service"
  type        = number
}

variable "oauth_client_id" {
  description = "Public identifier for the OAuth application."
  type        = string
}

variable "opensearch_endpoint" {
  description = "Domain-specific endpoint to submit OpenSearch requests."
  type        = string
}

variable "opensearch_username" {
  description = "Login username for the OpenSearch service.."
  type        = string
}

variable "postgres_password_secret_arn" {
  description = "The ARN of the self-managed postgres password secret."
  type        = string
}

variable "proxy_port" {
  description = "Port exposed by the reverse proxy."
  type        = number
}

variable "registry" {
  description = "The ECR registry containing task images."
  type        = string
}

variable "repository_arns" {
  description = "Identifers for the container repositories."
  type        = list(string)
}

variable "scaling_policy_type" {
  description = "Which method to use when scaling the cluster."
  type        = string
}

variable "secrets" {
  description = "A list of secrets as name/valueFrom 'Secret' objects."
  type        = map(map(string))
}

variable "secrets_arns" {
  description = "Identifers for managed secrets."
  type        = list(string)
}

variable "service" {
  description = "The service of the project/stack."
  type        = string
}

variable "service_desired_count" {
  description = "Number of ECS services running in parallel."
  type        = number
}

variable "scheduled_tasks" {
  description = "Data for scheduled tasks."
  type = object({
    cleartokens = object({
      assign_public_ip    = bool,
      is_enabled          = bool,
      schedule_expression = string,
    }),
    publish = object({
      assign_public_ip    = bool,
      is_enabled          = bool,
      schedule_expression = string,
    }),
  })
}

variable "sfn_backoff_rate" {
  description = "Multiplier that increases the retry interval on each attempt"
  type        = number
}

variable "sfn_heartbeat" {
  description = "How long between function 'heartbeats' before timeout (cannot exceed timeout)."
  type        = number
}

variable "sfn_max_attempts" {
  description = "Number of times to retry a failed function."
  type        = number
}

variable "sfn_retry_interval" {
  description = "How long to wait between function retries."
  type        = number
}

variable "sfn_timeout" {
  description = "The running time threshold for a function (must exceed heartbeat)."
  type        = number
}

variable "staticfiles_arn" {
  description = "Identifer for the static assets bucket."
  type        = string
}

variable "staticfiles_bucket" {
  description = "The name of the s3 bucket containing staticfiles."
  type        = string
}

variable "subnets" {
  description = "The (private) VPC subnets in which to register ECS."
  type        = list(string)
}

variable "tenant_domains" {
  description = "The origin(s) of the service."
  type        = set(string)
}

variable "threads" {
  description = "Number of gunicorn threads."
  type        = number
}

variable "web_port" {
  description = "The port exposed by the task container."
  type        = number
}

variable "wsgi" {
  description = "The entrypoint of the wsgi application."
  type        = string
}

variable "worker" {
  description = "The gunicorn worker type."
  type        = string
}

variable "worker_tmp" {
  description = "The gunicorn worker tmp directory."
  type        = string
}

variable "workers" {
  description = "How many gunicorn workers to spawn."
  type        = number
}
