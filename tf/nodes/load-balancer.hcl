# Instantiate the load-balancer module.

terraform {
  source = "../../../..//modules/infra/load-balancer/"
}

locals {
  env            = read_terragrunt_config(find_in_parent_folders("environment.hcl"))
  domain         = local.env.locals.domain
  environment    = local.env.locals.environment
  ports          = local.env.locals.ports
  tenant_domains = local.env.locals.tenant_domains
}

inputs = {
  additional_domains = local.tenant_domains
  alb_port           = local.ports.alb
  cidr_blocks        = "0.0.0.0/0",
  dns_ttl            = 60
  domain             = local.domain
  force_destroy      = contains(["development", "staging"], local.environment)
  health_check = {
    interval            = 200
    matcher             = 200
    path                = "/api/healthcheck/"
    threshold           = 3
    timeout             = 10
    unhealthy_threshold = 3
  }
  internal = false
  protocol = "tcp",
  ssl_port = local.ports.ssl
}
