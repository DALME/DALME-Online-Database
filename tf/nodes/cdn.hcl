# Inject the cdn module.

terraform {
  source = "../../../..//modules/infra/cdn/"
}

locals {
  env            = read_terragrunt_config(find_in_parent_folders("environment.hcl"))
  domain         = local.env.locals.domain
  environment    = local.env.locals.environment
  tenant_domains = local.env.locals.tenant_domains
}

inputs = {
  dns_ttl        = 60
  domain         = local.domain
  force_destroy  = contains(["development", "staging"], local.environment)
  price_class    = "PriceClass_100"
  tenant_domains = local.tenant_domains
}
