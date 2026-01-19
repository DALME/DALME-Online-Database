# Variables for the authorization module.

variable "lock_table" {
  description = "DynamoDB table holding terraform state locks."
  type        = string
}

variable "allowed_oidc" {
  description = "Github repos/branches allowed to assume to OIDC role."
  type        = list(map(string))
}
