# Entrypoint for the datastores module.

# RDS Postgres
module "postgres" {
  source = "../..//_reusable/rds/"

  allocated_storage                     = var.rds_postgres.allocated_storage
  apply_immediately                     = var.rds_postgres.apply_immediately
  backup_retention_period               = var.rds_postgres.backup_retention_period
  db_name                               = var.rds_postgres.db_name
  deletion_protection                   = var.rds_postgres.deletion_protection
  engine                                = var.rds_postgres.engine
  engine_version                        = var.rds_postgres.engine_version
  environment                           = var.environment
  iam_database_authentication_enabled   = var.rds_postgres.iam_database_authentication_enabled
  identifier                            = var.rds_postgres.identifier
  instance_class                        = var.rds_postgres.instance_class
  kms_key_arn                           = var.rds_postgres.storage_encrypted ? data.aws_kms_alias.global.target_key_arn : null
  manage_master_user_password           = var.rds_postgres.manage_master_user_password
  multi_az                              = var.rds_postgres.multi_az
  namespace                             = var.namespace
  parameter_rds_force_ssl               = var.rds_postgres.parameter_rds_force_ssl
  performance_insights_enabled          = var.rds_postgres.performance_insights_enabled
  performance_insights_retention_period = var.rds_postgres.performance_insights_retention_period
  port                                  = var.rds_postgres.port
  publicly_accessible                   = var.rds_postgres.publicly_accessible
  skip_final_snapshot                   = var.rds_postgres.skip_final_snapshot
  storage_encrypted                     = var.rds_postgres.storage_encrypted
  storage_type                          = var.rds_postgres.storage_type
  subnet_ids                            = data.aws_subnets.private.ids
  username                              = var.rds_postgres.username
  vpc_id                                = data.aws_vpc.this.id
}

resource "aws_security_group_rule" "postgres_ingress_jump_host" {
  description              = "Allow incoming traffic to postgres from the jump host."
  security_group_id        = module.postgres.security_group_id
  type                     = "ingress"
  protocol                 = "tcp"
  from_port                = var.rds_postgres.port
  to_port                  = var.rds_postgres.port
  source_security_group_id = data.aws_security_group.tunnel.id
}

resource "aws_security_group_rule" "jump_host_egress_postgres" {
  description              = "Allow outgoing traffic to postgres from the jump host."
  security_group_id        = data.aws_security_group.tunnel.id
  type                     = "egress"
  protocol                 = "tcp"
  from_port                = var.rds_postgres.port
  to_port                  = var.rds_postgres.port
  source_security_group_id = module.postgres.security_group_id
}

# Opensearch
locals {
  domain_name      = "${var.namespace}-${var.environment}-opensearch"
  master_user_name = "${var.namespace}-${var.environment}-opensearch-master-username"
}

module "opensearch_master_user_secret" {
  source = "../..//_reusable/secret/"

  name                   = "OPENSEARCH_MASTER_USER"
  description            = "Credentials for the Opensearch master user."
  environment            = var.environment
  keepers                = var.opensearch.keepers
  kms_key_arn            = data.aws_kms_alias.global.target_key_arn
  namespace              = var.namespace
  recovery_window        = var.opensearch.recovery_window
  username_password_pair = true
  username               = local.master_user_name
}

module "opensearch" {
  source = "../..//_reusable/opensearch/"

  admins                   = var.opensearch.admins
  aws_account              = var.aws_account
  aws_region               = var.aws_region
  custom_endpoint          = "opensearch.${var.domain}"
  dedicated_master_count   = var.opensearch.dedicated_master_count
  dedicated_master_enabled = var.opensearch.dedicated_master_enabled
  dns_ttl                  = var.opensearch.dns_ttl
  domain                   = var.domain
  domain_name              = local.domain_name
  ebs_enabled              = var.opensearch.ebs_enabled
  ebs_throughput           = var.opensearch.ebs_throughput
  ebs_volume_size          = var.opensearch.ebs_volume_size
  ebs_volume_type          = var.opensearch.ebs_volume_type
  encrypt_at_rest          = var.opensearch.encrypt_at_rest
  engine_version           = var.opensearch.engine_version
  environment              = var.environment
  instance_count           = var.opensearch.instance_count
  instance_type            = var.opensearch.instance_type
  keepers                  = var.opensearch.keepers
  kms_key_arn              = data.aws_kms_alias.global.target_key_arn
  log_retention_in_days    = var.opensearch.log_retention_in_days
  master_user_secret_arn   = module.opensearch_master_user_secret.version_arn
  namespace                = var.namespace
  node_to_node_encryption  = var.opensearch.node_to_node_encryption
  port                     = var.opensearch.port
  security_options_enabled = var.opensearch.security_options_enabled
  subnet_ids               = data.aws_subnets.private.ids
  zone_awareness_enabled   = var.opensearch.zone_awareness_enabled
  vpc_id                   = data.aws_vpc.this.id
}

# Security group rules.
resource "aws_security_group_rule" "opensearch_ingress" {
  security_group_id = module.opensearch.security_group_id
  type              = "ingress"
  description       = "Inbound HTTP from the VPC."
  protocol          = "tcp"
  from_port         = var.opensearch.port
  to_port           = var.opensearch.port
  cidr_blocks       = [data.aws_vpc.this.cidr_block]
}

resource "aws_security_group_rule" "opensearch_egress" {
  security_group_id = module.opensearch.security_group_id
  type              = "egress"
  description       = "Explicit ALLOW ALL outbound rule."
  protocol          = "-1"
  from_port         = 0
  to_port           = 0
  # tfsec:ignore:aws-ec2-no-public-egress-sgr
  cidr_blocks = ["0.0.0.0/0"]
  # tfsec:ignore:aws-ec2-no-public-egress-sgr
  ipv6_cidr_blocks = ["::/0"]
}

# Monitoring/alarms.
resource "aws_sns_topic" "opensearch_alarm" {
  name              = module.opensearch_alarm_sns_label.id
  kms_master_key_id = data.aws_kms_alias.global.target_key_arn

  delivery_policy = jsonencode({
    "http" : {
      "defaultHealthyRetryPolicy" : {
        "minDelayTarget" : 20,
        "maxDelayTarget" : 20,
        "numRetries" : 3,
        "numMaxDelayRetries" : 0,
        "numNoDelayRetries" : 0,
        "numMinDelayRetries" : 0,
        "backoffFunction" : "linear"
      },
      "disableSubscriptionOverrides" : false,
      "defaultThrottlePolicy" : {
        "maxReceivesPerSecond" : 1
      }
    }
  })

  tags = module.opensearch_alarm_sns_label.tags
}

resource "aws_sns_topic_subscription" "opensearch_alarm" {
  count     = length(var.opensearch.admins)
  topic_arn = aws_sns_topic.opensearch_alarm.arn
  protocol  = "email"
  endpoint  = var.opensearch.admins[count.index]
}

resource "aws_cloudwatch_metric_alarm" "opensearch_cpu_usage" {
  alarm_name  = module.opensearch_alarm_label.id
  metric_name = "CPUUtilization"
  namespace   = "AWS/ES"

  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = "5"
  period              = "60"
  statistic           = "Average"
  threshold           = "85"

  alarm_actions = [aws_sns_topic.opensearch_alarm.arn]

  dimensions = {
    DomainName = local.domain_name
    ClientId   = var.aws_account
  }

  tags = module.opensearch_alarm_label.tags
}

resource "aws_cloudwatch_metric_alarm" "opensearch_free_space" {
  alarm_name  = module.opensearch_alarm_label.id
  metric_name = "FreeStorageSpace"
  namespace   = "AWS/ES"

  comparison_operator = "LessThanThreshold"
  evaluation_periods  = "5"
  period              = "60"
  statistic           = "Minimum"
  threshold           = "5000"

  alarm_actions = [aws_sns_topic.opensearch_alarm.arn]

  dimensions = {
    DomainName = local.domain_name
    ClientId   = var.aws_account
  }

  tags = module.opensearch_alarm_label.tags
}

resource "aws_cloudwatch_metric_alarm" "opensearch_cluster_status" {
  alarm_name  = module.opensearch_alarm_label.id
  metric_name = "ClusterStatus.green"
  namespace   = "AWS/ES"

  comparison_operator = "LessThanThreshold"
  evaluation_periods  = "5"
  period              = "60"
  statistic           = "Average"
  threshold           = "1"

  alarm_actions = [aws_sns_topic.opensearch_alarm.arn]

  dimensions = {
    DomainName = local.domain_name
    ClientId   = var.aws_account
  }

  tags = module.opensearch_alarm_label.tags
}

resource "aws_cloudwatch_metric_alarm" "opensearch_cluster_nodes" {
  alarm_name  = module.opensearch_alarm_label.id
  metric_name = "Nodes"
  namespace   = "AWS/ES"

  comparison_operator = "LessThanThreshold"
  evaluation_periods  = "5"
  period              = "60"
  statistic           = "Average"
  threshold           = "2"
  treat_missing_data  = "notBreaching"

  alarm_actions = [aws_sns_topic.opensearch_alarm.arn]

  dimensions = {
    DomainName = local.domain_name
    ClientId   = var.aws_account
  }

  tags = module.opensearch_alarm_label.tags
}

resource "aws_cloudwatch_metric_alarm" "opensearch_cluster_memory" {
  alarm_name  = module.opensearch_alarm_label.id
  metric_name = "JVMMemoryPressure"
  namespace   = "AWS/ES"

  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = "3"
  period              = "300"
  threshold           = "88"
  statistic           = "Maximum"

  alarm_actions = [aws_sns_topic.opensearch_alarm.arn]

  dimensions = {
    DomainName = local.domain_name
    ClientId   = var.aws_account
  }

  tags = module.opensearch_alarm_label.tags
}
