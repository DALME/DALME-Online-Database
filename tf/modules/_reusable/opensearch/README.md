[Opensearch](https://aws.amazon.com/opensearch-service)

<!-- BEGIN_TF_DOCS -->
## Requirements

No requirements.

## Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | n/a |

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_opensearch_certificate_label"></a> [opensearch\_certificate\_label](#module\_opensearch\_certificate\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_opensearch_label"></a> [opensearch\_label](#module\_opensearch\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_opensearch_log_es_application_label"></a> [opensearch\_log\_es\_application\_label](#module\_opensearch\_log\_es\_application\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_opensearch_log_index_slow_label"></a> [opensearch\_log\_index\_slow\_label](#module\_opensearch\_log\_index\_slow\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_opensearch_log_label"></a> [opensearch\_log\_label](#module\_opensearch\_log\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_opensearch_log_policy_label"></a> [opensearch\_log\_policy\_label](#module\_opensearch\_log\_policy\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_opensearch_log_search_slow_label"></a> [opensearch\_log\_search\_slow\_label](#module\_opensearch\_log\_search\_slow\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_opensearch_service_linked_role_label"></a> [opensearch\_service\_linked\_role\_label](#module\_opensearch\_service\_linked\_role\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_opensearch_sg_label"></a> [opensearch\_sg\_label](#module\_opensearch\_sg\_label) | cloudposse/label/null | 0.25.0 |

## Resources

| Name | Type |
|------|------|
| [aws_acm_certificate.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/acm_certificate) | resource |
| [aws_acm_certificate_validation.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/acm_certificate_validation) | resource |
| [aws_cloudwatch_log_group.es_application](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_log_group) | resource |
| [aws_cloudwatch_log_group.index_slow](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_log_group) | resource |
| [aws_cloudwatch_log_group.search_slow](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_log_group) | resource |
| [aws_cloudwatch_log_resource_policy.log_policy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_log_resource_policy) | resource |
| [aws_iam_service_linked_role.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_service_linked_role) | resource |
| [aws_opensearch_domain.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/opensearch_domain) | resource |
| [aws_route53_record.cname](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/route53_record) | resource |
| [aws_route53_record.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/route53_record) | resource |
| [aws_security_group.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/security_group) | resource |
| [aws_iam_policy_document.log_policy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_route53_zone.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/route53_zone) | data source |
| [aws_secretsmanager_secret_version.master_user](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/secretsmanager_secret_version) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_admins"></a> [admins](#input\_admins) | Project admin email addresses. | `list(string)` | n/a | yes |
| <a name="input_aws_account"></a> [aws\_account](#input\_aws\_account) | The AWS account where resources are created. | `number` | n/a | yes |
| <a name="input_aws_region"></a> [aws\_region](#input\_aws\_region) | The AWS region where resources are created. | `string` | n/a | yes |
| <a name="input_custom_endpoint"></a> [custom\_endpoint](#input\_custom\_endpoint) | Fully qualified domain for your custom endpoint. | `string` | n/a | yes |
| <a name="input_dedicated_master_count"></a> [dedicated\_master\_count](#input\_dedicated\_master\_count) | Number of dedicated main nodes in the cluster. | `number` | n/a | yes |
| <a name="input_dedicated_master_enabled"></a> [dedicated\_master\_enabled](#input\_dedicated\_master\_enabled) | Whether dedicated main nodes are enabled for the cluster. | `bool` | n/a | yes |
| <a name="input_dedicated_master_type"></a> [dedicated\_master\_type](#input\_dedicated\_master\_type) | Instance type of the dedicated main nodes in the cluster. | `string` | `null` | no |
| <a name="input_dns_ttl"></a> [dns\_ttl](#input\_dns\_ttl) | Time to live for the certificate DNS record. | `number` | n/a | yes |
| <a name="input_domain"></a> [domain](#input\_domain) | The origin of the service. | `string` | n/a | yes |
| <a name="input_domain_name"></a> [domain\_name](#input\_domain\_name) | The domain name of the OpenSearch instance. | `string` | n/a | yes |
| <a name="input_ebs_enabled"></a> [ebs\_enabled](#input\_ebs\_enabled) | Whether EBS volumes are attached to data nodes. | `bool` | n/a | yes |
| <a name="input_ebs_throughput"></a> [ebs\_throughput](#input\_ebs\_throughput) | Specify the throughput (in MiB/s) of the EBS volumes attached to nodes. | `number` | n/a | yes |
| <a name="input_ebs_volume_size"></a> [ebs\_volume\_size](#input\_ebs\_volume\_size) | Size of EBS volumes attached to data nodes (in GiB). | `number` | n/a | yes |
| <a name="input_ebs_volume_type"></a> [ebs\_volume\_type](#input\_ebs\_volume\_type) | Type of EBS volumes attached to data nodes. | `string` | n/a | yes |
| <a name="input_encrypt_at_rest"></a> [encrypt\_at\_rest](#input\_encrypt\_at\_rest) | Whether to enable encryption at rest. | `bool` | n/a | yes |
| <a name="input_engine_version"></a> [engine\_version](#input\_engine\_version) | Which version of OpenSearch will the domain use. | `string` | n/a | yes |
| <a name="input_environment"></a> [environment](#input\_environment) | Identify the deployment environment. | `string` | n/a | yes |
| <a name="input_instance_count"></a> [instance\_count](#input\_instance\_count) | Number of instances in the cluster. | `number` | n/a | yes |
| <a name="input_instance_type"></a> [instance\_type](#input\_instance\_type) | Instance type of data nodes in the cluster. | `string` | n/a | yes |
| <a name="input_keepers"></a> [keepers](#input\_keepers) | Arbitrary key/value pairs that force secret regeneration on change. | <pre>object({<br/>    master_user_version = number<br/>  })</pre> | n/a | yes |
| <a name="input_kms_key_arn"></a> [kms\_key\_arn](#input\_kms\_key\_arn) | The project encryption key ARN. | `string` | n/a | yes |
| <a name="input_log_retention_in_days"></a> [log\_retention\_in\_days](#input\_log\_retention\_in\_days) | How long to keep OpenSearch logs. | `number` | n/a | yes |
| <a name="input_master_user_secret_arn"></a> [master\_user\_secret\_arn](#input\_master\_user\_secret\_arn) | ARN for the current OpenSearch master username/password secret version. | `string` | n/a | yes |
| <a name="input_namespace"></a> [namespace](#input\_namespace) | The project namespace. | `string` | n/a | yes |
| <a name="input_node_to_node_encryption"></a> [node\_to\_node\_encryption](#input\_node\_to\_node\_encryption) | Whether OpenSearch traffic is encrypted within the cluster. | `bool` | n/a | yes |
| <a name="input_port"></a> [port](#input\_port) | The bound port of the OpenSearch instance. | `number` | n/a | yes |
| <a name="input_security_options_enabled"></a> [security\_options\_enabled](#input\_security\_options\_enabled) | Whether or not fine-grained access control in enabled. | `bool` | n/a | yes |
| <a name="input_service"></a> [service](#input\_service) | An optional service namespace. | `string` | `null` | no |
| <a name="input_subnet_ids"></a> [subnet\_ids](#input\_subnet\_ids) | Private subnets for the cluster to occupy. | `list(any)` | n/a | yes |
| <a name="input_vpc_id"></a> [vpc\_id](#input\_vpc\_id) | Identifier for the VPC. | `string` | n/a | yes |
| <a name="input_zone_awareness_enabled"></a> [zone\_awareness\_enabled](#input\_zone\_awareness\_enabled) | If the cluster occupies multiple availability zones. | `bool` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_endpoint"></a> [endpoint](#output\_endpoint) | Domain-specific endpoint to submit OpenSearch requests. |
| <a name="output_label_context"></a> [label\_context](#output\_label\_context) | The root label context. |
| <a name="output_security_group_id"></a> [security\_group\_id](#output\_security\_group\_id) | Identify the security group controlling access to Opensearch. |
| <a name="output_security_group_label_context"></a> [security\_group\_label\_context](#output\_security\_group\_label\_context) | Label data for the Opensearch security group. |
<!-- END_TF_DOCS -->