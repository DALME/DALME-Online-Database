# Variables for the ssm module.

variable "aws_account" {
  description = "The AWS account where resources are created."
  type        = number
}

variable "environment" {
  description = "Identify the deployment environment."
  type        = string
}

variable "force_destroy" {
  description = "Whether deletion protection is active on the bucket."
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
