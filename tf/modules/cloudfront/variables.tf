# Terraform variables for the cloudfront module.

variable "alb_dns" {
  description = "Load balancer DNS endpoint."
  type        = string
}

variable "allowed_methods" {
  description = "Permissable HTTP verbs for this distribution."
  type        = list(string)
}

variable "aws_account" {
  description = "The AWS account where resources are created."
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

variable "force_destroy" {
  description = "Whether deletion protection is active on the module buckets."
  type        = bool
}

variable "service" {
  description = "The service of the project/stack."
  type        = string
}

variable "tenant_domains" {
  description = "The origin(s) of the service."
  type        = list(string)
}

variable "web_acl_id" {
  description = "Identifier for the WAF."
  type        = string
}
