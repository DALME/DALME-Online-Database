# Variables for the security module.

variable "allowed_roles" {
  description = "AWS assumed roles to be granted KMS key permissions."
  type        = list(string)
}
