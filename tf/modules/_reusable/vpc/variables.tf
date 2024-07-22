# Variables for the vpc module.

variable "az_count" {
  description = "Number of availability zones in a given region."
  type        = number
}

variable "cidr" {
  description = "The IPv4 CIDR block for the VPC."
  type        = string
}

variable "destination_cidr_block" {
  description = "The CIDR block associated with the local subnet."
  type        = string
}

variable "environment" {
  description = "Identify the deployment environment."
  type        = string
}

variable "log_destination" {
  description = "Optional ARN of a resource to receive VPC flow logs."
  type        = string
  default     = null
}

variable "log_destination_type" {
  description = " The type of the logging destination."
  type        = string
  default     = null
}

variable "namespace" {
  description = "The project namespace."
  type        = string
}
