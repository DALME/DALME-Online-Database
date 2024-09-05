# Labels for the opensearch module.

module "this_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  namespace   = var.namespace
  environment = var.environment
  name        = "opensearch"

  labels_as_tags = ["namespace", "environment", "name"]
}

module "this_label_certificate" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["ssl", "certificate"]

  context = module.this_label.context
}

module "this_label_sg" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["security", "group"]

  context = module.this_label.context
}

module "this_label_service_linked_role" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["service", "linked", "role"]

  context = module.this_label.context
}

module "this_label_log_policy" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["log", "policy"]

  context = module.this_label.context
}

module "this_label_log_es_application" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["es-application"]
  delimiter  = "/"

  context = module.this_label.context
}

module "this_label_log_index_slow" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["index-slow"]
  delimiter  = "/"

  context = module.this_label.context
}

module "this_label_log_search_slow" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  attributes = ["search-slow"]
  delimiter  = "/"

  context = module.this_label.context
}
