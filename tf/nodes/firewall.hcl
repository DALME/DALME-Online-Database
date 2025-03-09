# Inject the firewall module.

terraform {
  source = "../../../..//modules/infra/firewall/"
}

locals {
  env         = read_terragrunt_config(find_in_parent_folders("environment.hcl"))
  environment = local.env.locals.environment
}

inputs = {
  countries             = ["US"]
  force_destroy         = contains(["development", "staging"], local.environment)
  ipv4_ip_set_addresses = ["127.0.0.1/32"]
  ipv6_ip_set_addresses = ["2001:0db8:0000:0000:0000:0000:0000:0001/128"]
  rules = {
    domestic_dos_limit = 2000,
    global_dos_limit   = 500,
  }
}
