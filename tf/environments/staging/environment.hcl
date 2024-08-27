# Set common variables for this deployment stack.
#
# These values are automatically pulled in by the root terragrunt.hcl
# configuration and fed forward to the child modules when required.

locals {
  namespace   = "ida"
  environment = "staging"

  # AWS data
  aws_account = 905418315284
  admins = [
    "ops@ocp.systems",
  ]
  # NOTE: You can get this value by calling `aws sts get-caller-identity`
  # against whatever SSO profile you are using to invoke terraform.
  allowed_roles = [
    "arn:aws:sts::905418315284:assumed-role/AWSReservedSSO_AWSAdministratorAccess_f0b0802c3e187d9c/jhrr",
  ]

  # General infrastructure data
  gha_oidc_role_name = "gha-oidc-role"
  lock_table         = "terraform-locks"
  oauth_client_id    = "zzr1i8b3d4xqi3jb4lkro39r.ida.staging"
  ports = {
    alb        = 80
    mysql      = 3306
    opensearch = 443
    postgres   = 5432
    proxy      = 80
    ssl        = 443
    web        = 8080
  }

  # Tenant domain data
  domain = "ida.ocp.systems"
  tenant_domains = [
    "ida.ocp.systems",
    "dalme.ocp.systems",
    "pharmacopeias.ocp.systems",
  ]
}
