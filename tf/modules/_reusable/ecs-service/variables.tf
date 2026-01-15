# Variables for the ecs-service module.

variable "alb_target_group_arn" {
  description = "The ARN of the target group for the ALB."
  type        = string
}

variable "assign_public_ip" {
  description = "Should the service be exposed."
  type        = bool
}

variable "cluster" {
  description = "The ARN of the ECS cluster to run the service."
  type        = string
}

variable "cluster_name" {
  description = "The name of the ECS cluster running the service."
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

variable "deployment_circuit_breaker" {
  description = "Configure the deployment circuit breaker."
  type = object({
    enable   = bool
    rollback = bool
  })
  default = {
    enable   = false
    rollback = false
  }
}

variable "desired_count" {
  description = "Number of ECS services running in parallel."
  type        = number
}

variable "environment" {
  description = "Identify the deployment environment."
  type        = string
}

variable "force_new_deployment" {
  description = "Should an update to the service redeploy task definitions"
  type        = bool
}

variable "health_check_grace_period" {
  description = "How long to wait before terminating tasks that fail health checks."
  type        = number
}

variable "launch_type" {
  description = "What ECS mode the service should run in."
  type        = string
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

variable "namespace" {
  description = "The project namespace."
  type        = string
}

variable "proxy_name" {
  description = "Name of the proxy sidecar container."
  type        = string
}

variable "proxy_port" {
  description = "Port exposed by the reverse proxy."
  type        = number
}

variable "scaling_policy_type" {
  description = "Which method to use when scaling the cluster."
  type        = string
}

variable "scheduling_strategy" {
  description = "Scheduling strategy to use for the service."
  type        = string
}

variable "security_groups" {
  description = "The security groups mapped to the ECS service."
  type        = list(string)
}

variable "service" {
  description = "An optional service namespace."
  type        = string
  default     = null
}

variable "subnets" {
  description = "The (private) VPC subnets in which to register ECS."
  type        = list(string)
}

variable "task_definition" {
  description = "The ARN of the task to run on the service."
  type        = string
}
