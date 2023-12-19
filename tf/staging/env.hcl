# Set common variables for this environment (as determined by the subtree).
# This file is automatically pulled in in the root terragrunt.hcl configuration
# and fed forward to the child modules.
locals {
  account_ids = [
    "arn:aws:iam::800895234148:user/deploy",
  ]
  admins = [
    "ops@ocp.systems",
  ]
  aws_account        = 800895234148
  environment        = "staging"
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
  service = "dalme"
  tenant_domains = [
    # IMPORTANT: DALME must come first.
    "dalme.ocp.systems",
    "globalpharmacopeias.ocp.systems",
  ]
}
