# Entrypoint for the bucket module.
#
# This is just a wrapper around the terraform-aws-modules/s3-bucket/aws with a
# simplified interface and a couple of extra namespacing conveniences
# abstracted away. I've found that these are all the parameters I tend to use
# when using the module but if we need anything else we can just expose those
# parameters in our own variables.tf file and set them as necessary. This
# wrapper also has the virtue of clearing up the output naming convention
# which, on the original module, I find to be overly verbose and messy.
#
# https://github.com/terraform-aws-modules/terraform-aws-s3-bucket

locals {
  bucket = var.name_prefix != null ? module.bucket_prefix_label.id : module.bucket_label.id
  tags   = var.name_prefix != null ? module.bucket_prefix_label.tags : module.bucket_label.tags
}

# tfsec:ignore:aws-s3-enable-bucket-encryption tfsec:ignore:aws-s3-enable-bucket-logging tfsec:ignore:aws-s3-enable-versioning tfsec:ignore:aws-s3-encryption-customer-key
module "this" {
  source  = "terraform-aws-modules/s3-bucket/aws"
  version = "4.1.2"

  bucket                               = local.bucket
  acl                                  = var.acl
  block_public_acls                    = var.block_public_acls
  block_public_policy                  = var.block_public_policy
  control_object_ownership             = var.control_object_ownership
  cors_rule                            = var.cors_rules
  force_destroy                        = var.force_destroy
  ignore_public_acls                   = var.ignore_public_acls
  lifecycle_rule                       = var.lifecycle_rule
  logging                              = var.logging
  object_ownership                     = var.object_ownership
  restrict_public_buckets              = var.restrict_public_buckets
  server_side_encryption_configuration = var.server_side_encryption_configuration
  versioning                           = var.versioning
  website                              = var.website

  tags = local.tags
}
