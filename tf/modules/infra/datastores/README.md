# Datastores

<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | ~> 1.6 |
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | 5.59.0 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | 5.59.0 |

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_opensearch"></a> [opensearch](#module\_opensearch) | ../..//_reusable/opensearch/ | n/a |
| <a name="module_opensearch_alarm_label"></a> [opensearch\_alarm\_label](#module\_opensearch\_alarm\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_opensearch_alarm_sns_label"></a> [opensearch\_alarm\_sns\_label](#module\_opensearch\_alarm\_sns\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_opensearch_master_user_secret"></a> [opensearch\_master\_user\_secret](#module\_opensearch\_master\_user\_secret) | ../..//_reusable/secret/ | n/a |
| <a name="module_postgres"></a> [postgres](#module\_postgres) | ../..//_reusable/rds/ | n/a |

## Resources

| Name | Type |
|------|------|
| [aws_cloudwatch_metric_alarm.opensearch_cluster_memory](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/resources/cloudwatch_metric_alarm) | resource |
| [aws_cloudwatch_metric_alarm.opensearch_cluster_nodes](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/resources/cloudwatch_metric_alarm) | resource |
| [aws_cloudwatch_metric_alarm.opensearch_cluster_status](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/resources/cloudwatch_metric_alarm) | resource |
| [aws_cloudwatch_metric_alarm.opensearch_cpu_usage](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/resources/cloudwatch_metric_alarm) | resource |
| [aws_cloudwatch_metric_alarm.opensearch_free_space](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/resources/cloudwatch_metric_alarm) | resource |
| [aws_security_group_rule.jump_host_egress_postgres](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/resources/security_group_rule) | resource |
| [aws_security_group_rule.opensearch_egress](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/resources/security_group_rule) | resource |
| [aws_security_group_rule.opensearch_ingress](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/resources/security_group_rule) | resource |
| [aws_security_group_rule.postgres_ingress_jump_host](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/resources/security_group_rule) | resource |
| [aws_sns_topic.opensearch_alarm](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/resources/sns_topic) | resource |
| [aws_sns_topic_subscription.opensearch_alarm](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/resources/sns_topic_subscription) | resource |
| [aws_kms_alias.global](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/data-sources/kms_alias) | data source |
| [aws_security_group.tunnel](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/data-sources/security_group) | data source |
| [aws_subnets.private](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/data-sources/subnets) | data source |
| [aws_vpc.this](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/data-sources/vpc) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_domain"></a> [domain](#input\_domain) | The origin of the service. | `string` | n/a | yes |
| <a name="input_opensearch"></a> [opensearch](#input\_opensearch) | Configuration for managing an instance of opensearch. | <pre>object({<br>    admins                   = list(string)<br>    dedicated_master_count   = number<br>    dedicated_master_enabled = bool<br>    dns_ttl                  = number<br>    ebs_enabled              = bool<br>    ebs_throughput           = number<br>    ebs_volume_size          = number<br>    ebs_volume_type          = string<br>    encrypt_at_rest          = bool<br>    engine_version           = string<br>    instance_count           = number<br>    instance_type            = string<br>    keepers                  = object({ master_user_version = number })<br>    log_retention_in_days    = number<br>    node_to_node_encryption  = bool<br>    port                     = number<br>    recovery_window          = number<br>    security_options_enabled = bool<br>    zone_awareness_enabled   = bool<br>  })</pre> | n/a | yes |
| <a name="input_rds_postgres"></a> [rds\_postgres](#input\_rds\_postgres) | Configuration for an RDS instance. | <pre>object({<br>    allocated_storage                     = number<br>    apply_immediately                     = bool<br>    backup_retention_period               = number<br>    cidr_blocks                           = string<br>    db_name                               = string<br>    deletion_protection                   = bool<br>    engine                                = string<br>    engine_version                        = number<br>    iam_database_authentication_enabled   = bool<br>    identifier                            = string<br>    instance_class                        = string<br>    ipv6_cidr_blocks                      = string<br>    manage_master_user_password           = bool<br>    multi_az                              = bool<br>    parameter_rds_force_ssl               = bool<br>    performance_insights_enabled          = bool<br>    performance_insights_retention_period = number<br>    port                                  = number<br>    publicly_accessible                   = bool<br>    skip_final_snapshot                   = bool<br>    storage_encrypted                     = bool<br>    storage_type                          = string<br>    username                              = string<br>  })</pre> | n/a | yes |

## Outputs

No outputs.
<!-- END_TF_DOCS -->