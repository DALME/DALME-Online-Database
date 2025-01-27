# Variables for the ec2-instance module.

variable "ami_filters" {
  description = "One or more name/value pairs to filter down the ami data source."
  type        = list(object({ name = string, values = list(string) }))
  default     = null
}

variable "ami_most_recent" {
  description = "If more than one ami result is returned, use the most recent."
  type        = bool
  default     = true
}

variable "ami_name_regex" {
  description = "Regex for filtering down the ami data source."
  type        = string
}

variable "ami_owners" {
  description = "List of AMI owners for filtering down the ami data source"
  type        = list(string)
  default     = ["amazon"]
}

variable "environment" {
  description = "Identify the deployment environment."
  type        = string
}

variable "iam_instance_profile_name" {
  description = "The IAM Instance Profile to attach to the instance."
  type        = string
}

variable "instance_type" {
  description = "The type of the ec2 instance."
  type        = string
}

variable "name" {
  description = "The name of the launch template."
  type        = string
}

variable "monitoring" {
  description = "Should the EC2 instance have detailed monitoring enabled."
  type        = bool
  default     = true
}

variable "metadata_options" {
  description = "Metadata configuration for the instance."
  type = object({
    http_endpoint               = string,
    http_put_response_hop_limit = number,
    http_protocol_ipv6          = optional(string),
    instance_metadata_tags      = string
  })
}

variable "network_interfaces" {
  description = "Attach one or more network interfaces to the instance."
  type = list(object({
    associate_public_ip_address = bool,
    delete_on_termination       = bool,
    security_groups             = optional(list(string)),
    subnet_id                   = optional(string),
  }))
  default = null
}

variable "namespace" {
  description = "The project namespace."
  type        = string
}

variable "update_default_version" {
  description = "Bump the default version of the instance on each update."
  type        = bool
  default     = true
}

variable "vpc_id" {
  description = "Identifier for the VPC."
  type        = string
}
