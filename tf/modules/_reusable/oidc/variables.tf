# Variables for the oidc module.

variable "environment" {
  description = "Identify the deployment environment."
  type        = string
}

variable "gha_oidc_role_name" {
  description = "Name of the github action OIDC role."
  type        = string
}

variable "gha_oidc_policy_name" {
  description = "Name of the github action OIDC role."
  type        = string
  default     = "gha-oidc-policy"
}

variable "oidc_allowed" {
  description = "Github org/repos/branches allowed to assume to OIDC role."
  type        = list(map(string))
}

variable "namespace" {
  description = "The project namespace."
  type        = string
}
