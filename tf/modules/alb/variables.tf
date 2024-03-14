# Terraform variables for the alb module.

variable "alb_port" {
  description = "Load balancer listening port."
  type        = number
}

variable "dns_ttl" {
  description = "Time to live for the certificate DNS record."
  type        = number
}

variable "environment" {
  description = "Identify the deployment environment."
  type        = string
}

variable "health_check_path" {
  description = "Application smoke test endpoint."
  type        = string
}

variable "health_check_interval" {
  description = "Frequency (secs) of the health checks"
  type        = number
}

variable "health_check_matcher" {
  description = "HTTP status code indicating a passing health check."
  type        = number
}

variable "health_check_threshold" {
  description = "Health check count before considering an unhealthy target healthy."
  type        = number
}

variable "health_check_timeout" {
  description = "Time (secs) without a response indicting a failed health check."
  type        = number
}

variable "health_check_unhealthy_threshold" {
  description = "Consecutive failed health checks before considering a target unhealthy."
  type        = number
}

variable "service" {
  description = "The service of the project/stack."
  type        = string
}

variable "ssl_port" {
  description = "Secure HTTPS listening port."
  type        = number
}

variable "security_groups" {
  description = "The security group for the alb."
  type        = list(string)
}

variable "subnets" {
  description = "The (public) VPC subnets in which to register the ALB."
  type        = list(string)
}

variable "tenant_domains" {
  description = "The origin(s) of the service."
  type        = list(string)
}

variable "vpc_id" {
  description = "Identifier for the VPC."
  type        = string
}
