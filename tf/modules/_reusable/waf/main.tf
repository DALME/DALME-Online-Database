# Entrypoint for the waf module.
#
# This module only handles "CLOUDFRONT" scoped firewalls, which is currently
# our only use-case.

locals {
  scope = "CLOUDFRONT"
}

resource "aws_wafv2_ip_set" "ipv4" {
  name               = module.waf_ipv4_label.name
  scope              = local.scope
  ip_address_version = "IPV4"
  addresses          = var.ipv4_ip_set_addresses

  tags = module.waf_ipv4_label.tags
}

resource "aws_wafv2_ip_set" "ipv6" {
  name               = module.waf_ipv6_label.name
  scope              = local.scope
  ip_address_version = "IPV6"
  addresses          = var.ipv6_ip_set_addresses

  tags = module.waf_ipv6_label.tags
}

resource "aws_wafv2_web_acl" "this" {
  name  = module.waf_label.name
  scope = local.scope

  default_action {
    allow {}
  }

  visibility_config {
    cloudwatch_metrics_enabled = true
    metric_name                = var.name
    sampled_requests_enabled   = true
  }

  rule {
    name     = "AWSRateBasedRuleDomesticDOS"
    priority = 1

    action {
      block {}
    }

    statement {
      rate_based_statement {
        limit              = var.rules.domestic_dos_limit
        aggregate_key_type = "IP"

        scope_down_statement {
          geo_match_statement {
            country_codes = var.countries
          }
        }
      }
    }
    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "AWSRateBasedRuleDomesticDOS"
      sampled_requests_enabled   = true
    }
  }

  rule {
    name     = "AWSRateBasedRuleGlobalDOS"
    priority = 2

    action {
      block {}
    }

    statement {
      rate_based_statement {
        limit              = var.rules.global_dos_limit
        aggregate_key_type = "IP"

        scope_down_statement {
          not_statement {
            statement {
              geo_match_statement {
                country_codes = var.countries
              }
            }
          }
        }
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "AWSRateBasedRuleGlobalDOS"
      sampled_requests_enabled   = true
    }
  }

  rule {
    name     = "AWSIPBlackList"
    priority = 3

    action {
      block {}
    }

    statement {
      or_statement {
        statement {
          ip_set_reference_statement {
            arn = aws_wafv2_ip_set.ipv4.arn
          }
        }
        statement {
          ip_set_reference_statement {
            arn = aws_wafv2_ip_set.ipv6.arn
          }
        }
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "AWSIPBlackList"
      sampled_requests_enabled   = true
    }
  }

  # AWS managed rules.
  rule {
    name     = "AWSManagedRulesCommonRuleSet"
    priority = 10

    override_action {
      count {}
    }

    statement {
      managed_rule_group_statement {
        name        = "AWSManagedRulesCommonRuleSet"
        vendor_name = "AWS"
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "AWSManagedRulesCommonRuleSetMetric"
      sampled_requests_enabled   = true
    }
  }

  rule {
    name     = "AWSManagedRulesKnownBadInputsRuleSet"
    priority = 20

    override_action {
      count {}
    }

    statement {
      managed_rule_group_statement {
        name        = "AWSManagedRulesKnownBadInputsRuleSet"
        vendor_name = "AWS"
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "AWSManagedRulesKnownBadInputsRuleSetMetric"
      sampled_requests_enabled   = true
    }
  }

  rule {
    name     = "AWSManagedRulesAmazonIpReputationList"
    priority = 30

    override_action {
      count {}
    }

    statement {
      managed_rule_group_statement {
        name        = "AWSManagedRulesAmazonIpReputationList"
        vendor_name = "AWS"
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "AWSManagedRulesAmazonIpReputationListMetric"
      sampled_requests_enabled   = true
    }
  }

  rule {
    name     = "AWSManagedRulesAnonymousIpList"
    priority = 40

    override_action {
      count {}
    }

    statement {
      managed_rule_group_statement {
        name        = "AWSManagedRulesAnonymousIpList"
        vendor_name = "AWS"
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "AWSManagedRulesAnonymousIpListMetric"
      sampled_requests_enabled   = true
    }
  }

  rule {
    name     = "AWSManagedRulesSQLiRuleSet"
    priority = 50

    override_action {
      count {}
    }

    statement {
      managed_rule_group_statement {
        name        = "AWSManagedRulesSQLiRuleSet"
        vendor_name = "AWS"
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "AWSManagedRulesSQLiRuleSetMetric"
      sampled_requests_enabled   = true
    }
  }

  rule {
    name     = "AWSManagedRulesLinuxRuleSet"
    priority = 60

    override_action {
      count {}
    }

    statement {
      managed_rule_group_statement {
        name        = "AWSManagedRulesLinuxRuleSet"
        vendor_name = "AWS"
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "AWSManagedRulesLinuxRuleSetMetric"
      sampled_requests_enabled   = true
    }
  }

  rule {
    name     = "AWSManagedRulesUnixRuleSet"
    priority = 70

    override_action {
      count {}
    }

    statement {
      managed_rule_group_statement {
        name        = "AWSManagedRulesUnixRuleSet"
        vendor_name = "AWS"
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "AWSManagedRulesUnixRuleSetMetric"
      sampled_requests_enabled   = true
    }
  }

  tags = module.waf_label.tags
}

resource "aws_wafv2_web_acl_logging_configuration" "this" {
  log_destination_configs = [var.log_destination_configs]
  resource_arn            = aws_wafv2_web_acl.this.arn
}
