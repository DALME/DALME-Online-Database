# IDA IaC

This module defines all the Terraform and Terragrunt code necessary for
provisioning an IDA deploy environment on AWS. Taken along with the Github
Actions workflows, this implements a fully automated CI/CD process for the
service.

One caveat to the above is that any deploy environment should be manually
provisioned for the first time as there are some bootstrapping details that are
not 100% accounted for (eg. certain secrets must be created by hand as they
access legacy services or APIs not under control of our IaC). Once this has
been performed however, all subsequent infrastructure and code deploys should
not require any administrator intervention (unforeseen bugs notwithstanding).

## Initializing a Deploy Environment