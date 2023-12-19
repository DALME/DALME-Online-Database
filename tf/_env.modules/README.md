# Terragrunt Modules

This directory contains Terragrunt `.hcl` definitions that instantiate our
reusable Terraform modules. That is to say, the actual module entrypoints where
values are provided to the modules for provisioning. Thinking in terms of the
dependency tree, these files represent the terminating nodes.
