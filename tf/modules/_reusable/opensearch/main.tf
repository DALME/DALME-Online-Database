# Entrypoint for the opensearch module.

locals {
  subnet_ids   = slice(var.subnet_ids, 0, var.instance_count)
  resource_arn = "arn:aws:es:${var.aws_region}:${var.aws_account}:domain/${var.domain_name}"
}

# https://docs.aws.amazon.com/opensearch-service/latest/developerguide/slr-aos.html
resource "aws_iam_service_linked_role" "this" {
  aws_service_name = "opensearchservice.amazonaws.com"
  description      = "AWSServiceRoleForAmazonOpenSearchService"

  tags = module.opensearch_service_linked_role_label.tags
}

# Logs - https://docs.aws.amazon.com/AWSJavaSDK/latest/javadoc/com/amazonaws/services/elasticsearch/model/LogType.html
resource "aws_cloudwatch_log_group" "es_application" {
  name              = module.opensearch_log_es_application_label.id
  kms_key_id        = var.kms_key_arn
  retention_in_days = var.log_retention_in_days

  tags = module.opensearch_log_es_application_label.tags
}

resource "aws_cloudwatch_log_group" "index_slow" {
  name              = module.opensearch_log_index_slow_label.id
  kms_key_id        = var.kms_key_arn
  retention_in_days = var.log_retention_in_days

  tags = module.opensearch_log_index_slow_label.tags
}

resource "aws_cloudwatch_log_group" "search_slow" {
  name              = module.opensearch_log_search_slow_label.id
  kms_key_id        = var.kms_key_arn
  retention_in_days = var.log_retention_in_days

  tags = module.opensearch_log_search_slow_label.tags
}

data "aws_iam_policy_document" "log_policy" {
  statement {
    actions = [
      "logs:CreateLogStream",
      "logs:PutLogEvents",
      "logs:PutLogEventsBatch",
    ]

    resources = [
      "${aws_cloudwatch_log_group.index_slow.arn}:*",
      "${aws_cloudwatch_log_group.search_slow.arn}:*",
      "${aws_cloudwatch_log_group.es_application.arn}:*"
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
      values   = [local.resource_arn]
    }
  }
}

resource "aws_cloudwatch_log_resource_policy" "log_policy" {
  policy_document = data.aws_iam_policy_document.log_policy.json
  policy_name     = module.opensearch_log_policy_label.id
}

resource "aws_security_group" "this" {
  description = "Security group for the OpenSearch instance."
  name_prefix = module.opensearch_sg_label.id
  vpc_id      = var.vpc_id

  lifecycle {
    create_before_destroy = true
  }

  tags = module.opensearch_sg_label.tags
}

data "aws_secretsmanager_secret_version" "master_user" {
  secret_id = var.master_user_secret_arn
}

locals {
  master_user_credentials = jsondecode(data.aws_secretsmanager_secret_version.master_user.secret_string)
}

resource "aws_opensearch_domain" "this" {
  domain_name    = var.domain_name
  engine_version = var.engine_version

  depends_on = [
    aws_iam_service_linked_role.this,
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
      master_user_name     = local.master_user_credentials["username"]
      master_user_password = local.master_user_credentials["password"]
    }
  }

  domain_endpoint_options {
    enforce_https       = true
    tls_security_policy = "Policy-Min-TLS-1-2-2019-07"

    custom_endpoint_enabled         = true
    custom_endpoint                 = var.custom_endpoint
    custom_endpoint_certificate_arn = var.certificate_arn
  }

  ebs_options {
    ebs_enabled = var.ebs_enabled
    volume_size = var.ebs_volume_size
    volume_type = var.ebs_volume_type
    throughput  = var.ebs_throughput
  }

  encrypt_at_rest {
    enabled = var.encrypt_at_rest
  }

  log_publishing_options {
    cloudwatch_log_group_arn = aws_cloudwatch_log_group.index_slow.arn
    log_type                 = "INDEX_SLOW_LOGS"
  }

  log_publishing_options {
    cloudwatch_log_group_arn = aws_cloudwatch_log_group.search_slow.arn
    log_type                 = "SEARCH_SLOW_LOGS"
  }

  log_publishing_options {
    cloudwatch_log_group_arn = aws_cloudwatch_log_group.es_application.arn
    log_type                 = "ES_APPLICATION_LOGS"
  }

  node_to_node_encryption {
    enabled = var.node_to_node_encryption
  }

  vpc_options {
    subnet_ids         = local.subnet_ids
    security_group_ids = [aws_security_group.this.id]
  }

  access_policies = <<CONFIG
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": "es:*",
            "Principal": "*",
            "Effect": "Allow",
            "Resource": "${local.resource_arn}/*"
        }
    ]
}
CONFIG

  tags = module.opensearch_label.tags
}
