# Variables for the secret module.

variable "description" {
  description = "A description of the secret."
  type        = string
  default     = null
}

variable "environment" {
  description = "Identify the deployment environment."
  type        = string
}

variable "keepers" {
  description = "Define values that on change will force regeneration of the random value."
  type        = map(any)
}

variable "kms_key_arn" {
  description = "ARN of thw KMS key to be used to encrypt the secret."
  type        = string
}

variable "length" {
  description = "The length of the generated random password"
  type        = number
  default     = 64
}

variable "min_special" {
  description = "Minimum number of special characters."
  type        = number
  default     = 5
}

variable "name" {
  description = "The name of the new secret."
  type        = string
}

variable "override_special" {
  description = "Supply special characters to use for use in random strings."
  type        = string
  default     = "!@#$%&*()-_=+[]{}<>:?"
}

variable "recovery_window" {
  description = "Number of days that must elapse before a secret can be deleted."
  type        = number
}

variable "region" {
  description = "Region for replicating the secret."
  type        = string
  default     = null
}

variable "service" {
  description = "An optional service namespace."
  type        = string
  default     = null
}

variable "username" {
  description = "The username for a username/password blob."
  type        = string
  default     = null
}

variable "username_password_pair" {
  description = "If true, the password will be in username/password blob format."
  type        = bool
}
