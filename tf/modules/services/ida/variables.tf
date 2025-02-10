# Variables for the ida module.

variable "admins" {
  description = "Project admin email addresses."
  type        = list(string)
}

variable "allowed_hosts" {
  description = "Permitted domains for requests."
  type        = list(string)
}

variable "app_port" {
  description = "The port exposed by the app container."
  type        = number
}

variable "assign_public_ip" {
  description = "Should the service be exposed."
  type        = bool
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

variable "domain" {
  description = "The origin of the service."
  type        = string
}

variable "fargate_cpu" {
  description = "Fargate instance CPU units to provision (1 vCPU = 1024 CPU units)."
  type        = number
}

variable "force_delete" {
  description = "Activate deletion protection on this service's ECR repositories."
  type        = bool
}

variable "fargate_memory" {
  description = "Fargate instance memory to provision (in MiB)."
  type        = number
}

variable "force_new_deployment" {
  description = "Should an update to the service redeploy task definitions"
  type        = bool
}

variable "gunicorn_config" {
  description = "Path to the gunicorn config file."
  type        = string
}

variable "health_check_grace_period" {
  description = "How long to wait before terminating tasks that fail health checks."
  type        = number
}

variable "images" {
  description = "Container repository names for this service."
  type        = list(string)
}

variable "keepers" {
  description = "Arbitrary key/value pairs that force secret regeneration on change."
  type = object({
    admin_user_version          = number
    django_secret_key_version   = number
    oauth_client_secret_version = number
  })
}

variable "launch_type" {
  description = "What ECS mode the service should run in."
  type        = string
}

variable "log_level" {
  description = "Set the severity of the app logger."
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
  description = "Identifier for the OAuth 2.0 client."
  type        = string
}

variable "opensearch_master_user_secret_name" {
  description = "Identifies the Opensearch master user secret."
  type        = string
}

variable "postgres_version" {
  description = "The release version of the rds postgres instance."
  type        = number
}

variable "proxy_port" {
  description = "Port exposed by the reverse proxy."
  type        = number
}

variable "recovery_window" {
  description = "How many days to preserve deleted secrets before shredding."
  type        = number
}

variable "retain_n" {
  description = "The number of container images to retain for this service."
  type        = number
}

variable "scaling_policy_type" {
  description = "Which method to use when scaling the cluster."
  type        = string
}

variable "scheduled_tasks" {
  description = "Data for scheduled tasks."
  type = object({
    cleartokens = object({
      assign_public_ip    = bool,
      state               = string,
      schedule_expression = string,
    }),
    publish = object({
      assign_public_ip    = bool,
      state               = string,
      schedule_expression = string,
    }),
  })
}

variable "scheduling_strategy" {
  description = "Scheduling strategy to use for the service."
  type        = string
}

variable "service_desired_count" {
  description = "Number of ECS services running in parallel."
  type        = number
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

variable "tenant_domains" {
  description = "The tenanted origin(s) of the service."
  type        = list(string)
}

variable "threads" {
  description = "Number of gunicorn threads."
  type        = number
}

variable "unmanaged_suffix" {
  description = "Label that indicates some resource is unmanaged (rare)."
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

variable "wsgi" {
  description = "The entrypoint of the wsgi application."
  type        = string
}
