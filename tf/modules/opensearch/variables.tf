# Terraform variables for the opensearch module.

variable "admins" {
  description = "Project admin email addresses."
  type        = list(string)
}

variable "aws_account" {
  description = "The AWS account where resources are created."
  type        = number
}

variable "aws_region" {
  description = "The AWS region where resources are created."
  type        = string
}

variable "dedicated_master_enabled" {
  description = "Whether dedicated main nodes are enabled for the cluster."
  type        = bool
}

variable "dedicated_master_count" {
  description = "Number of dedicated main nodes in the cluster."
  type        = number
}

variable "dedicated_master_type" {
  description = "Instance type of the dedicated main nodes in the cluster."
  type        = string
}

variable "dns_ttl" {
  description = "Time to live for the certificate DNS record."
  type        = number
}

variable "ebs_enabled" {
  description = "Whether EBS volumes are attached to data nodes."
  type        = bool
}

variable "ebs_throughput" {
  description = "Specify the throughput (in MiB/s) of the EBS volumes attached to nodes."
  type        = number
}

variable "ebs_volume_size" {
  description = "Size of EBS volumes attached to data nodes (in GiB)."
  type        = number
}

variable "ebs_volume_type" {
  description = "Type of EBS volumes attached to data nodes."
  type        = string
}

variable "encrypt_at_rest" {
  description = "Whether to enable encryption at rest."
  type        = bool
}

variable "engine_version" {
  description = "Which version of OpenSearch will the domain use."
  type        = string
}

variable "environment" {
  description = "Identify the deployment environment."
  type        = string
}

variable "instance_type" {
  description = "Instance type of data nodes in the cluster."
  type        = string
}

variable "instance_count" {
  description = "Number of instances in the cluster."
  type        = number
}

variable "kms_key_arn" {
  description = "The project encryption key ARN."
  type        = string
}

variable "log_retention_in_days" {
  description = "How long to keep OpenSearch logs."
  type        = number
}

variable "node_to_node_encryption" {
  description = "Whether OpenSearch traffic is encrypted within the cluster."
  type        = bool
}

variable "master_user_password" {
  description = "Password for the OpenSearch master user."
  type        = string
}

variable "security_group_ids" {
  description = "Security groups for the cluster."
  type        = list(string)
}

variable "security_options_enabled" {
  description = "Whether or not fine-grained access control in enabled."
  type        = bool
}

variable "service" {
  description = "The service of the project/stack."
  type        = string
}

variable "subnet_ids" {
  description = "Private subnets for the cluster to occupy."
  type        = list(any)
}

variable "tenant_domains" {
  description = "The origin(s) of the service."
  type        = list(string)
}

variable "zone_awareness_enabled" {
  description = "If the cluster occupies multiple availability zones."
  type        = bool
}
