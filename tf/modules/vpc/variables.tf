# Terraform variables for the vpc module.

variable "account_ids" {
  description = "AWS accounts granted jump server permissions."
  type        = list(string)
}

variable "aws_account" {
  description = "The AWS account where resources are created."
  type        = number
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

variable "environment" {
  description = "Identify the deployment environment."
  type        = string
}

variable "force_destroy" {
  description = "Whether deletion protection is active on the module buckets."
  type        = bool
}

variable "security_groups" {
  description = "Common data for instantiating security groups."
  type = object({
    cidr_blocks      = string,
    ipv6_cidr_blocks = string,
    protocol         = string,
    opensearch_port  = number,
    postgres_port    = number,
    proxy_port       = number,
    ssl_port         = number,
  })
}

variable "service" {
  description = "The service of the project/stack."
  type        = string
}
