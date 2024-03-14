# Terraform variables for the waf module.

variable "aws_account" {
  description = "The AWS account where resources are created."
  type        = number
}

variable "country" {
  description = "A country code for scoping geo rules."
  type        = string
}

variable "environment" {
  description = "Identify the deployment environment."
  type        = string
}

variable "force_destroy" {
  description = "Whether deletion protection is active on the module buckets."
  type        = bool
}

variable "name" {
  description = "The name of the WAF instance."
  type        = string
}

variable "service" {
  description = "The service of the project/stack."
  type        = string
}
