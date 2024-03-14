# Set common variables for this environment (as determined by the subtree).
# This file is automatically pulled in in the root terragrunt.hcl configuration
# and fed forward to the child modules.
locals {
  aws_account = ""
  domain      = "dalme.org"
  environment = "production"
  service     = "dalme"
}
