# Set common variables for this deployment stack.
#
# These values are automatically pulled in by the root terragrunt.hcl
# configuration and fed forward to the child modules when required.

locals {
  namespace   = "ida"
  environment = "staging"

  aws_account = 209330743443
  admins = [
    "pizzorno@fas.harvard.edu",
    "jhrr@ocp.systems",
  ]
  # NOTE: You can get this value by calling `aws sts get-caller-identity`
  # against whatever SSO profile you are using to invoke terraform.
  allowed_roles = [
    "arn:aws:sts::${local.aws_account}:assumed-role/AWSReservedSSO_AWSAdministratorAccess_e91761712d542b1e/pizzorno",
    "arn:aws:sts::${local.aws_account}:assumed-role/AWSReservedSSO_AWSAdministratorAccess_e91761712d542b1e/jhrr",
  ]
  allowed_oidc = [
    { org = "DALME", repo = "DALME-Online-Database", branch = "development.v2" },
  ]
  aws_dns_writer_role_name = "DNSWriterRole"

  lock_table                         = "terraform-locks"
  oauth_client_id                    = "zzr1i8b3d4xqi3jb4lkro39r.ida.staging"
  postgres_version                   = 16
  opensearch_version                 = "Elasticsearch_7.7"
  opensearch_master_user_secret_name = "OPENSEARCH-MASTER-USER"
  unmanaged_suffix                   = "UNMANAGED"

  ports = {
    alb        = 80
    mysql      = 3306
    opensearch = 443
    postgres   = 5432
    proxy      = 80
    ssl        = 443
    app        = 8080
  }

  # Tenant domains.
  domain = "documentaryarchaeology.net"
  tenant_domains = [
    "documentaryarchaeology.net",
    "dalme-beta.org",
    "historical-pharmacopeias.org",
  ]
}
