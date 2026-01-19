# Variables for the oidc module.

variable "allowed" {
  description = "Github org/repos/branches allowed to assume to OIDC role."
  type        = list(map(string))
}

variable "environment" {
  description = "Identify the deployment environment."
  type        = string
}

variable "provider_name" {
  description = "Name of the github action OIDC provider resource."
  type        = string
  default     = "oidc-github-actions-provider"
}

variable "role_name" {
  description = "Name of the github action OIDC role."
  type        = string
  default     = "OIDCGithubActionsRole"
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
