# Terraform definitions for the opensearch module.

terraform {
  required_version = "~> 1.3"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.14.0"
    }
  }
}

locals {
  domain            = var.tenant_domains[0]
  opensearch_domain = "${var.service}-opensearch-${var.environment}"
  master_user_name  = "${var.service}-master-${var.environment}"
  subnet_ids        = slice(var.subnet_ids, 0, var.instance_count)
  custom_endpoint   = "opensearch.${local.domain}"
}

# Certificate
data "aws_route53_zone" "main" {
  name = local.domain
}

resource "aws_acm_certificate" "opensearch" {
  domain_name       = local.custom_endpoint
  validation_method = "DNS"

  lifecycle {
    create_before_destroy = true
  }

  tags = {
    Name = "${var.service}-opensearch-certificate-${var.environment}"
  }
}

resource "aws_acm_certificate_validation" "opensearch" {
  certificate_arn = aws_acm_certificate.opensearch.arn
  validation_record_fqdns = [
    for record in aws_route53_record.opensearch : record.fqdn
  ]
}

resource "aws_route53_record" "opensearch" {
  for_each = {
    for dvo in aws_acm_certificate.opensearch.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }

  allow_overwrite = true
  name            = each.value.name
  records         = [each.value.record]
  ttl             = var.dns_ttl
  type            = each.value.type
  zone_id         = data.aws_route53_zone.main.zone_id
}

# DNS canonical name record for the ES service/dashboard.
resource "aws_route53_record" "opensearch_cname" {
  zone_id = data.aws_route53_zone.main.zone_id
  name    = "opensearch.${data.aws_route53_zone.main.name}"
  type    = "CNAME"
  ttl     = "300"

  records = [aws_opensearch_domain.main.endpoint]
}

# https://docs.aws.amazon.com/opensearch-service/latest/developerguide/slr-aos.html
resource "aws_iam_service_linked_role" "opensearch" {
  aws_service_name = "opensearchservice.amazonaws.com"
  description      = "AWSServiceRoleForAmazonOpenSearchService"

  tags = {
    Name = "${var.service}-opensearch-service-linked-role-${var.environment}"
  }
}

# Logs - https://docs.aws.amazon.com/AWSJavaSDK/latest/javadoc/com/amazonaws/services/elasticsearch/model/LogType.html
resource "aws_cloudwatch_log_group" "opensearch_log_group_index_slow_logs" {
  name              = "${var.service}-logs-opensearch-${local.opensearch_domain}-index-slow-${var.environment}"
  kms_key_id        = var.kms_key_arn
  retention_in_days = var.log_retention_in_days

  tags = {
    Name = "${var.service}-logs-opensearch-${local.opensearch_domain}-index-slow-${var.environment}"
  }
}

resource "aws_cloudwatch_log_group" "opensearch_log_group_search_slow_logs" {
  name              = "${var.service}-logs-opensearch-${local.opensearch_domain}-search-slow-${var.environment}"
  kms_key_id        = var.kms_key_arn
  retention_in_days = var.log_retention_in_days

  tags = {
    Name = "${var.service}-logs-opensearch-${local.opensearch_domain}-search-slow-${var.environment}"
  }
}

resource "aws_cloudwatch_log_group" "opensearch_log_group_es_application_logs" {
  name              = "${var.service}-logs-opensearch-${local.opensearch_domain}-es-application-${var.environment}"
  kms_key_id        = var.kms_key_arn
  retention_in_days = var.log_retention_in_days

  tags = {
    Name = "${var.service}-logs-opensearch-${local.opensearch_domain}-es-application-${var.environment}"
  }
}

data "aws_iam_policy_document" "opensearch_log_policy" {
  statement {
    actions = [
      "logs:CreateLogStream",
      "logs:PutLogEvents",
      "logs:PutLogEventsBatch",
    ]

    resources = [
      "${aws_cloudwatch_log_group.opensearch_log_group_index_slow_logs.arn}:*",
      "${aws_cloudwatch_log_group.opensearch_log_group_search_slow_logs.arn}:*",
      "${aws_cloudwatch_log_group.opensearch_log_group_es_application_logs.arn}:*"
    ]

    principals {
      identifiers = ["es.amazonaws.com"]
      type        = "Service"
    }

    condition {
      test     = "StringEquals"
      variable = "aws:SourceAccount"
      values   = [var.aws_account]
    }

    condition {
      test     = "ArnLike"
      variable = "aws:SourceArn"
      values   = ["arn:aws:es:${var.aws_region}:${var.aws_account}:domain/${local.opensearch_domain}"]
    }
  }
}

resource "aws_cloudwatch_log_resource_policy" "opensearch_log_policy" {
  policy_document = data.aws_iam_policy_document.opensearch_log_policy.json
  policy_name     = "${var.service}-opensearch-log-policy-${var.environment}"
}

# TODO: Don't activate until we are ready to migrate.
# import {
#   count = var.environment == "production" ? 1 : 0
#   to    = aws_opensearch_domain.main
#   id    = local.opensearch_domain
# }

resource "aws_opensearch_domain" "main" {
  domain_name    = local.opensearch_domain
  engine_version = var.engine_version

  depends_on = [
    aws_acm_certificate_validation.opensearch,
    aws_iam_service_linked_role.opensearch,
  ]

  cluster_config {
    dedicated_master_count   = var.dedicated_master_count
    dedicated_master_type    = var.dedicated_master_type
    dedicated_master_enabled = var.dedicated_master_enabled
    instance_type            = var.instance_type
    instance_count           = var.instance_count
    zone_awareness_enabled   = var.zone_awareness_enabled

    dynamic "zone_awareness_config" {
      for_each = var.zone_awareness_enabled ? [len(local.subnet_ids)] : []
      content {
        availability_zone_count = zone_awareness_config.value
      }
    }
  }

  # https://docs.aws.amazon.com/opensearch-service/latest/developerguide/fgac.html
  advanced_security_options {
    enabled                        = var.security_options_enabled
    anonymous_auth_enabled         = true
    internal_user_database_enabled = true

    master_user_options {
      master_user_name     = local.master_user_name
      master_user_password = var.master_user_password
    }
  }

  encrypt_at_rest {
    enabled = var.encrypt_at_rest
  }

  domain_endpoint_options {
    enforce_https       = true
    tls_security_policy = "Policy-Min-TLS-1-2-2019-07"

    custom_endpoint_enabled         = true
    custom_endpoint                 = local.custom_endpoint
    custom_endpoint_certificate_arn = aws_acm_certificate.opensearch.arn
  }

  ebs_options {
    ebs_enabled = var.ebs_enabled
    volume_size = var.ebs_volume_size
    volume_type = var.ebs_volume_type
    throughput  = var.ebs_throughput
  }

  log_publishing_options {
    cloudwatch_log_group_arn = aws_cloudwatch_log_group.opensearch_log_group_index_slow_logs.arn
    log_type                 = "INDEX_SLOW_LOGS"
  }

  log_publishing_options {
    cloudwatch_log_group_arn = aws_cloudwatch_log_group.opensearch_log_group_search_slow_logs.arn
    log_type                 = "SEARCH_SLOW_LOGS"
  }

  log_publishing_options {
    cloudwatch_log_group_arn = aws_cloudwatch_log_group.opensearch_log_group_es_application_logs.arn
    log_type                 = "ES_APPLICATION_LOGS"
  }

  node_to_node_encryption {
    enabled = var.node_to_node_encryption
  }

  vpc_options {
    subnet_ids         = local.subnet_ids
    security_group_ids = var.security_group_ids
  }

  access_policies = <<CONFIG
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": "es:*",
            "Principal": "*",
            "Effect": "Allow",
            "Resource": "arn:aws:es:${var.aws_region}:${var.aws_account}:domain/${local.domain}/*"
        }
    ]
}
CONFIG

  tags = {
    Name = local.opensearch_domain
  }
}
