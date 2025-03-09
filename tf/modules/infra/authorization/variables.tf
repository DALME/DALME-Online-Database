# Variables for the authorization module.

variable "gha_oidc_role_name" {
  description = "Name of the github action OIDC role."
  type        = string
}

variable "lock_table" {
  description = "DynamoDB table holding terraform state locks."
  type        = string
}

variable "oidc_allowed" {
  description = "Github repos/branches allowed to assume to OIDC role."
  type        = list(map(string))
}
