# Variables for the alb module.

variable "alb_port" {
  description = "Load balancer listening port."
  type        = number
}

variable "dns_ttl" {
  description = "Time to live for the certificate's DNS record."
  type        = number
}

variable "domain" {
  description = "The origin of the service."
  type        = string
}

variable "environment" {
  description = "Identify the deployment environment."
  type        = string
}

variable "health_check" {
  description = "Parameters configuring the ALB's healthcheck."
  type = object({
    interval            = number, # Frequency (secs) of the health checks.
    matcher             = number, # HTTP status code indicating a passing health check.
    path                = string, # URL route of the healthcheck.
    threshold           = number, # Count before considering an unhealthy target healthy.
    timeout             = number, # Time (secs) without a response indicting a failed health check.
    unhealthy_threshold = number, # Consecutive failed health checks before considering a target unhealthy.
  })
}

variable "internal" {
  description = "Should this ALB have a public IP or not."
  type        = bool
}

variable "namespace" {
  description = "The project namespace."
  type        = string
}

variable "service" {
  description = "An optional service namespace."
  type        = string
  default     = null
}

variable "ssl_port" {
  description = "Secure HTTPS listening port."
  type        = number
}

variable "subnets" {
  description = "Public subnets of the VPC."
  type        = list(string)
}

variable "vpc_id" {
  description = "Identifier for the VPC."
  type        = string
}
