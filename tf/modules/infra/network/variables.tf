# Variables for the network module.

variable "allowed_roles" {
  description = "AWS users/roles granted jump server permissions."
  type        = list(string)
}

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

variable "force_destroy" {
  description = "Whether deletion protection is active on the module buckets."
  type        = bool
}

variable "ssl_port" {
  description = "Port for making SSL connections."
  type        = number
}
