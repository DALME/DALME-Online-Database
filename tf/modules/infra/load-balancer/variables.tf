# Variables for the load-balancer module.

variable "alb_port" {
  description = "Load balancer listening port."
  type        = number
}

variable "cidr_blocks" {
  description = "IPv4 range for the ALB security groups."
  type        = string
}

variable "dns_ttl" {
  description = "Time to live for the certificate DNS record."
  type        = number
}

variable "domain" {
  description = "The origin of the service."
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

variable "ipv6_cidr_blocks" {
  description = "IPv6 range for the ALB security groups."
  type        = string
}

variable "protocol" {
  description = "Transport protocol for the security group."
  type        = string
}

variable "proxy_port" {
  description = "Reverse proxy listening port."
  type        = number
}

variable "ssl_port" {
  description = "Secure HTTPS listening port."
  type        = number
}
