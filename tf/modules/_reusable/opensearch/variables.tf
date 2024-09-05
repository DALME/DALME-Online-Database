# Variables for the opensearch module.

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

variable "custom_endpoint" {
  description = "Fully qualified domain for your custom endpoint."
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
  default     = null
}

variable "dns_ttl" {
  description = "Time to live for the certificate DNS record."
  type        = number
}

variable "domain" {
  description = "The origin of the service."
  type        = string
}

variable "domain_name" {
  description = "The domain name of the OpenSearch instance."
  type        = string
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

variable "keepers" {
  description = "Arbitrary key/value pairs that force secret regeneration on change."
  type = object({
    master_user_version = number
  })
}

variable "kms_key_arn" {
  description = "The project encryption key ARN."
  type        = string
}

variable "log_retention_in_days" {
  description = "How long to keep OpenSearch logs."
  type        = number
}

variable "master_user_secret_arn" {
  description = "ARN for the current OpenSearch master username/password secret version."
  type        = string
}

variable "namespace" {
  description = "The project namespace."
  type        = string
}

variable "node_to_node_encryption" {
  description = "Whether OpenSearch traffic is encrypted within the cluster."
  type        = bool
}

variable "port" {
  description = "The bound port of the OpenSearch instance."
  type        = number
}

variable "security_options_enabled" {
  description = "Whether or not fine-grained access control in enabled."
  type        = bool
}

variable "service" {
  description = "An optional service namespace."
  type        = string
  default     = null
}

variable "subnet_ids" {
  description = "Private subnets for the cluster to occupy."
  type        = list(any)
}

variable "vpc_id" {
  description = "Identifier for the VPC."
  type        = string
}

variable "zone_awareness_enabled" {
  description = "If the cluster occupies multiple availability zones."
  type        = bool
}
