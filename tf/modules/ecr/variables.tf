# Terraform variables for the ecr module.

variable "force_delete" {
  description = "Whether to activate deletion protection on the repositories."
  type        = bool
}

variable "image" {
  description = "Common container name."
  type        = string
}

variable "images" {
  description = "Application container sub-service names."
  type        = list(string)
}

variable "kms_key_arn" {
  description = "The project encryption key ARN."
  type        = string
}
