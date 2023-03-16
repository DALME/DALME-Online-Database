# Cloudwatch alarms for the opensearch module.

resource "aws_sns_topic" "opensearch_alarm" {
  name              = "${var.service}-sns-opensearch-alarm-${var.environment}"
  kms_master_key_id = var.kms_key_arn
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

  tags = {
    Name = "${var.service}-sns-opensearch-alarm-${var.environment}"
  }
}

resource "aws_sns_topic_subscription" "opensearch_alarm" {
  count     = length(var.admins)
  topic_arn = aws_sns_topic.opensearch_alarm.arn
  protocol  = "email"
  endpoint  = var.admins[count.index]
}

resource "aws_cloudwatch_metric_alarm" "opensearch_cpu_usage" {
  alarm_name  = "${var.service}-opensearch-cloudwatch-cpu-usage-${var.environment}"
  metric_name = "CPUUtilization"
  namespace   = "AWS/ES"

  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = "5"
  period              = "60"
  statistic           = "Average"
  threshold           = "85"

  alarm_actions = [aws_sns_topic.opensearch_alarm.arn]

  dimensions = {
    DomainName = local.opensearch_domain
    ClientId   = var.aws_account
  }

  tags = {
    Name = "${var.service}-opensearch-cloudwatch-cpu-usage-${var.environment}"
  }
}

resource "aws_cloudwatch_metric_alarm" "opensearch_free_space" {
  alarm_name  = "${var.service}-opensearch-cloudwatch-free-space-${var.environment}"
  metric_name = "FreeStorageSpace"
  namespace   = "AWS/ES"

  comparison_operator = "LessThanThreshold"
  evaluation_periods  = "5"
  period              = "60"
  statistic           = "Minimum"
  threshold           = "5000"

  alarm_actions = [aws_sns_topic.opensearch_alarm.arn]

  dimensions = {
    DomainName = local.opensearch_domain
    ClientId   = var.aws_account
  }

  tags = {
    Name = "${var.service}-opensearch-cloudwatch-free-space-${var.environment}"
  }
}

resource "aws_cloudwatch_metric_alarm" "opensearch_cluster_status" {
  alarm_name  = "${var.service}-opensearch-cloudwatch-cluster-status-${var.environment}"
  metric_name = "ClusterStatus.green"
  namespace   = "AWS/ES"

  comparison_operator = "LessThanThreshold"
  evaluation_periods  = "5"
  period              = "60"
  statistic           = "Average"
  threshold           = "1"

  alarm_actions = [aws_sns_topic.opensearch_alarm.arn]

  dimensions = {
    DomainName = local.opensearch_domain
    ClientId   = var.aws_account
  }

  tags = {
    Name = "${var.service}-opensearch-cloudwatch-cluster-status-${var.environment}"
  }
}

resource "aws_cloudwatch_metric_alarm" "opensearch_cluster_nodes" {
  alarm_name  = "${var.service}-opensearch-cloudwatch-cluster-nodes-${var.environment}"
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
    DomainName = local.opensearch_domain
    ClientId   = var.aws_account
  }

  tags = {
    Name = "${var.service}-opensearch-cloudwatch-cluster-nodes-${var.environment}"
  }
}

resource "aws_cloudwatch_metric_alarm" "opensearch_cluster_memory" {
  alarm_name  = "${var.service}-opensearch-cloudwatch-cluster-memory-${var.environment}"
  metric_name = "JVMMemoryPressure"
  namespace   = "AWS/ES"

  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = "3"
  period              = "300"
  threshold           = "88"
  statistic           = "Maximum"

  alarm_actions = [aws_sns_topic.opensearch_alarm.arn]

  dimensions = {
    DomainName = local.opensearch_domain
    ClientId   = var.aws_account
  }

  tags = {
    Name = "${var.service}-opensearch-cloudwatch-cluster-memory-${var.environment}"
  }
}
