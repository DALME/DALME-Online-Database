# Labels for the firewall module.

module "waf_logs_label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  namespace   = var.namespace
  environment = var.environment
  name        = "aws-waf-logs"

  attributes = [var.aws_account]

  # CAUTION: The log destination must begin with an 'aws-waf-logs-' prefix so
  # we shuffle things arouns here to ensure that is the case.
  label_order = ["name", "namespace", "environment", "attributes"]

  labels_as_tags = ["name"]

  context = module.waf_label.context
}
