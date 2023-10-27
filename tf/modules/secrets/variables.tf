# Terraform variables for the secrets module.

variable "account_ids" {
  description = "AWS accounts to be granted KMS key permissions."
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

variable "environment" {
  description = "Identify the deployment environment."
  type        = string
}

variable "keeper" {
  description = "Increment this value to regenerate random secrets."
  type        = number
}

variable "recovery_window" {
  description = "How many days to preserve deleted secrets before shredding."
  type        = number
}

variable "secrets" {
  description = "A list of secrets names."
  type        = list(string)
}

variable "service" {
  description = "The service of the project/stack."
  type        = string
}

variable "static_secrets" {
  description = "Designate secrets that don't change."
  type        = list(string)
}
