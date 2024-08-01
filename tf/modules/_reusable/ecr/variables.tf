# Variables for the ecr module.

variable "environment" {
  description = "Identify the deployment environment."
  type        = string
}

variable "force_delete" {
  description = "Whether to activate deletion protection on the repositories."
  type        = bool
}

variable "image" {
  description = "Application component of the container name."
  type        = string
}

variable "kms_key_arn" {
  description = "The project encryption key ARN."
  type        = string
}

variable "retain_n" {
  description = "The number of images to retain."
  type        = number
}

variable "service" {
  description = "An optional service namespace."
  type        = string
  default     = null
}
