# Labels for the opensearch module.

module "opensearch_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  namespace   = var.namespace
  environment = var.environment
  name        = "opensearch"

  labels_as_tags = ["namespace", "environment", "name"]
}

module "opensearch_sg_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["security", "group"]

  context = module.opensearch_label.context
}

module "opensearch_service_linked_role_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["service", "linked", "role"]

  context = module.opensearch_label.context
}

module "opensearch_log_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["log"]

  context = module.opensearch_label.context
}

module "opensearch_log_policy_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["policy"]

  context = module.opensearch_log_label.context
}

module "opensearch_log_es_application_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["es-application"]
  delimiter  = "/"

  context = module.opensearch_log_label.context
}

module "opensearch_log_index_slow_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["index-slow"]
  delimiter  = "/"

  context = module.opensearch_log_label.context
}

module "opensearch_log_search_slow_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["search-slow"]
  delimiter  = "/"

  context = module.opensearch_log_label.context
}
