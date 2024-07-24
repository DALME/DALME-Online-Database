# Variables for the bucket module.

variable "acl" {
  description = "The canned ACL to apply to the bucket."
  type        = string
  default     = null
}

variable "aws_account" {
  description = "The AWS account where resources are created."
  type        = number
}

variable "block_public_acls" {
  description = "Switch to block public ACLs for this bucket."
  type        = bool
  default     = true
}

variable "block_public_policy" {
  description = "Switch to block public bucket policies for this bucket."
  type        = bool
  default     = true
}

variable "control_object_ownership" {
  description = "Whether to manage S3 Bucket Ownership Controls on this bucket."
  type        = bool
  default     = false
}

variable "cors_rules" {
  description = "List of maps configuring the bucket CORS policy."
  type        = any
  default     = []
}

variable "environment" {
  description = "Identify the deployment environment."
  type        = string
}

variable "force_destroy" {
  description = "Whether deletion protection is active on the bucket."
  type        = bool
}

variable "ignore_public_acls" {
  description = "Switch to ignore public ACLs for this bucket."
  type        = bool
  default     = true
}

variable "lifecycle_rule" {
  description = "List of maps defining bucket lifecycle managment."
  type        = any
  default     = []
}

variable "logging" {
  description = "A map containing log configuration for bucket access."
  type        = any
  default     = {}
}

variable "name" {
  description = "The name of the bucket. Will be augmented with namespace data."
  type        = string
}

variable "namespace" {
  description = "The project namespace."
  type        = string
}

variable "object_ownership" {
  description = "Controls the ownership mode of the objects uploaded to your bucket."
  type        = string
  default     = "BucketOwnerEnforced"
}

variable "restrict_public_buckets" {
  description = "Switch to restrict public bucket policies for this bucket."
  type        = bool
  default     = true
}

variable "server_side_encryption_configuration" {
  description = "Map configuring server-side encryption configuration for the bucket."
  type        = any
  default     = {}
}

variable "service" {
  description = "An optional service namespace."
  type        = string
  default     = null
}

variable "website" {
  description = "Map containing static website hosting configuration."
  type        = any
  default     = {}
}

variable "versioning" {
  description = "A map configuring bucket versioning."
  type        = map(string)
  default     = {}
}
