# Labels for the datastores module.

module "opensearch_alarm_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["alarm"]

  context = module.opensearch.label_context
}

module "opensearch_alarm_sns_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["sns"]

  context = module.opensearch.label_context
}

module "opensearch_sg_ingress_vpc_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["ingress", "vpc"]

  context = module.opensearch.security_group_label_context
}

module "postgres_sg_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["postgres"]

  context = module.postgres.security_group_label_context
}

module "postgres_sg_egress_jump_host_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["egress", "jump-host"]

  context = module.postgres_sg_label.context
}

module "postgres_sg_ingress_jump_host_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["ingress", "jump-host"]

  context = module.postgres_sg_label.context
}
