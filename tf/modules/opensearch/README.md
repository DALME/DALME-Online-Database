<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | ~> 1.3 |
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | 5.14.0 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | 5.14.0 |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [aws_acm_certificate.opensearch](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/acm_certificate) | resource |
| [aws_acm_certificate_validation.opensearch](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/acm_certificate_validation) | resource |
| [aws_cloudwatch_log_group.opensearch_log_group_es_application_logs](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/cloudwatch_log_group) | resource |
| [aws_cloudwatch_log_group.opensearch_log_group_index_slow_logs](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/cloudwatch_log_group) | resource |
| [aws_cloudwatch_log_group.opensearch_log_group_search_slow_logs](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/cloudwatch_log_group) | resource |
| [aws_cloudwatch_log_resource_policy.opensearch_log_policy](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/cloudwatch_log_resource_policy) | resource |
| [aws_cloudwatch_metric_alarm.opensearch_cluster_memory](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/cloudwatch_metric_alarm) | resource |
| [aws_cloudwatch_metric_alarm.opensearch_cluster_nodes](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/cloudwatch_metric_alarm) | resource |
| [aws_cloudwatch_metric_alarm.opensearch_cluster_status](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/cloudwatch_metric_alarm) | resource |
| [aws_cloudwatch_metric_alarm.opensearch_cpu_usage](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/cloudwatch_metric_alarm) | resource |
| [aws_cloudwatch_metric_alarm.opensearch_free_space](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/cloudwatch_metric_alarm) | resource |
| [aws_iam_service_linked_role.opensearch](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/iam_service_linked_role) | resource |
| [aws_opensearch_domain.main](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/opensearch_domain) | resource |
| [aws_route53_record.opensearch](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/route53_record) | resource |
| [aws_route53_record.opensearch_cname](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/route53_record) | resource |
| [aws_sns_topic.opensearch_alarm](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/sns_topic) | resource |
| [aws_sns_topic_subscription.opensearch_alarm](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/sns_topic_subscription) | resource |
| [aws_iam_policy_document.opensearch_log_policy](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/data-sources/iam_policy_document) | data source |
| [aws_route53_zone.main](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/data-sources/route53_zone) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_admins"></a> [admins](#input\_admins) | Project admin email addresses. | `list(string)` | n/a | yes |
| <a name="input_aws_account"></a> [aws\_account](#input\_aws\_account) | The AWS account where resources are created. | `number` | n/a | yes |
| <a name="input_aws_region"></a> [aws\_region](#input\_aws\_region) | The AWS region where resources are created. | `string` | n/a | yes |
| <a name="input_dedicated_master_count"></a> [dedicated\_master\_count](#input\_dedicated\_master\_count) | Number of dedicated main nodes in the cluster. | `number` | n/a | yes |
| <a name="input_dedicated_master_enabled"></a> [dedicated\_master\_enabled](#input\_dedicated\_master\_enabled) | Whether dedicated main nodes are enabled for the cluster. | `bool` | n/a | yes |
| <a name="input_dedicated_master_type"></a> [dedicated\_master\_type](#input\_dedicated\_master\_type) | Instance type of the dedicated main nodes in the cluster. | `string` | n/a | yes |
| <a name="input_dns_ttl"></a> [dns\_ttl](#input\_dns\_ttl) | Time to live for the certificate DNS record. | `number` | n/a | yes |
| <a name="input_ebs_enabled"></a> [ebs\_enabled](#input\_ebs\_enabled) | Whether EBS volumes are attached to data nodes. | `bool` | n/a | yes |
| <a name="input_ebs_throughput"></a> [ebs\_throughput](#input\_ebs\_throughput) | Specify the throughput (in MiB/s) of the EBS volumes attached to nodes. | `number` | n/a | yes |
| <a name="input_ebs_volume_size"></a> [ebs\_volume\_size](#input\_ebs\_volume\_size) | Size of EBS volumes attached to data nodes (in GiB). | `number` | n/a | yes |
| <a name="input_ebs_volume_type"></a> [ebs\_volume\_type](#input\_ebs\_volume\_type) | Type of EBS volumes attached to data nodes. | `string` | n/a | yes |
| <a name="input_encrypt_at_rest"></a> [encrypt\_at\_rest](#input\_encrypt\_at\_rest) | Whether to enable encryption at rest. | `bool` | n/a | yes |
| <a name="input_engine_version"></a> [engine\_version](#input\_engine\_version) | Which version of OpenSearch will the domain use. | `string` | n/a | yes |
| <a name="input_environment"></a> [environment](#input\_environment) | Identify the deployment environment. | `string` | n/a | yes |
| <a name="input_instance_count"></a> [instance\_count](#input\_instance\_count) | Number of instances in the cluster. | `number` | n/a | yes |
| <a name="input_instance_type"></a> [instance\_type](#input\_instance\_type) | Instance type of data nodes in the cluster. | `string` | n/a | yes |
| <a name="input_kms_key_arn"></a> [kms\_key\_arn](#input\_kms\_key\_arn) | The project encryption key ARN. | `string` | n/a | yes |
| <a name="input_log_retention_in_days"></a> [log\_retention\_in\_days](#input\_log\_retention\_in\_days) | How long to keep OpenSearch logs. | `number` | n/a | yes |
| <a name="input_master_user_password"></a> [master\_user\_password](#input\_master\_user\_password) | Password for the OpenSearch master user. | `string` | n/a | yes |
| <a name="input_node_to_node_encryption"></a> [node\_to\_node\_encryption](#input\_node\_to\_node\_encryption) | Whether OpenSearch traffic is encrypted within the cluster. | `bool` | n/a | yes |
| <a name="input_security_group_ids"></a> [security\_group\_ids](#input\_security\_group\_ids) | Security groups for the cluster. | `list(string)` | n/a | yes |
| <a name="input_security_options_enabled"></a> [security\_options\_enabled](#input\_security\_options\_enabled) | Whether or not fine-grained access control in enabled. | `bool` | n/a | yes |
| <a name="input_service"></a> [service](#input\_service) | The service of the project/stack. | `string` | n/a | yes |
| <a name="input_subnet_ids"></a> [subnet\_ids](#input\_subnet\_ids) | Private subnets for the cluster to occupy. | `list(string)` | n/a | yes |
| <a name="input_tenant_domains"></a> [tenant\_domains](#input\_tenant\_domains) | The origin(s) of the service. | `list(string)` | n/a | yes |
| <a name="input_zone_awareness_enabled"></a> [zone\_awareness\_enabled](#input\_zone\_awareness\_enabled) | If the cluster occupies multiple availability zones. | `bool` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_endpoint"></a> [endpoint](#output\_endpoint) | Domain-specific endpoint to submit OpenSearch requests. |
| <a name="output_master_user_name"></a> [master\_user\_name](#output\_master\_user\_name) | Login user for the OpenSearch service. |
<!-- END_TF_DOCS -->