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
