# Instantiate the load-balancer module.

terraform {
  source = "../../../..//modules/infra/load-balancer/"
}

locals {
  env         = read_terragrunt_config(find_in_parent_folders("environment.hcl"))
  domain      = local.env.locals.domain
  environment = local.env.locals.environment
  ports       = local.env.locals.ports
}

inputs = {
  alb_port         = local.ports.alb
  cidr_blocks      = "0.0.0.0/0",
  domain           = local.domain
  dns_ttl          = 60
  internal         = false
  ipv6_cidr_blocks = "::/0",
  health_check = {
    interval            = 200
    matcher             = 200
    path                = "/api/ping/"
    threshold           = 3
    timeout             = 10
    unhealthy_threshold = 3
  }
  protocol   = "tcp",
  proxy_port = local.ports.proxy
  ssl_port   = local.ports.ssl
}
