# Terraform variables for the oidc module.

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

variable "gha_oidc_role_name" {
  description = "Name of the github action OIDC role."
  type        = string
}

variable "oidc_allowed" {
  description = "Github repos/branches allowed to assume to OIDC role."
  type        = list(map(string))
}

variable "lock_table" {
  description = "DynamoDB table holding terraform state locks."
  type        = string
}

variable "service" {
  description = "The service of the project/stack."
  type        = string
}
