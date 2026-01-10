# Variables for the alb module.

variable "alb_port" {
  description = "Load balancer listening port."
  type        = number
}

variable "certificate_arn" {
  description = "Reference to the SSL certificate encrypting traffic."
  type        = string
}

variable "dns_ttl" {
  description = "Time to live for the certificate's DNS record."
  type        = number
}

variable "environment" {
  description = "Identify the deployment environment."
  type        = string
}

variable "force_destroy" {
  description = "Whether deletion protection is active on buckets."
  type        = bool
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

variable "logging_enabled" {
  description = "Should this ALB write to logs."
  type        = bool
}

variable "log_destination" {
  description = "Bucket to hold the ALB access logs."
  type        = string
}

variable "log_prefix" {
  description = "String to prepend to the S3 bucket destination."
  type        = string
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
