Virtual Private Network

<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | ~> 1.6 |
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | 5.70.0 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | 5.70.0 |

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_jump_host"></a> [jump\_host](#module\_jump\_host) | ../..//_reusable/ec2-instance/ | n/a |
| <a name="module_network_jh_asg_label"></a> [network\_jh\_asg\_label](#module\_network\_jh\_asg\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_network_jh_policy_label"></a> [network\_jh\_policy\_label](#module\_network\_jh\_policy\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_network_jh_profile_label"></a> [network\_jh\_profile\_label](#module\_network\_jh\_profile\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_network_jh_role_label"></a> [network\_jh\_role\_label](#module\_network\_jh\_role\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_network_label"></a> [network\_label](#module\_network\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_session_manager"></a> [session\_manager](#module\_session\_manager) | ../..//_reusable/ssm/ | n/a |
| <a name="module_vpc"></a> [vpc](#module\_vpc) | ../..//_reusable/vpc/ | n/a |
| <a name="module_vpc_flow_logs"></a> [vpc\_flow\_logs](#module\_vpc\_flow\_logs) | ../..//_reusable/bucket/ | n/a |

## Resources

| Name | Type |
|------|------|
| [aws_autoscaling_group.jump_host](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/resources/autoscaling_group) | resource |
| [aws_iam_instance_profile.jump_host_profile](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/resources/iam_instance_profile) | resource |
| [aws_iam_policy.jump_host_policy_ssm](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/resources/iam_policy) | resource |
| [aws_iam_role.jump_host_role](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/resources/iam_role) | resource |
| [aws_iam_role_policy_attachment.jump_host_ssm](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/resources/iam_role_policy_attachment) | resource |
| [aws_s3_bucket_policy.ssm_logs](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/resources/s3_bucket_policy) | resource |
| [aws_security_group_rule.jump_host_egress_https](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/resources/security_group_rule) | resource |
| [aws_iam_policy_document.jump_host_policy_assume](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.jump_host_policy_ssm](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.ssm_logs](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/data-sources/iam_policy_document) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_allowed_roles"></a> [allowed\_roles](#input\_allowed\_roles) | AWS users/roles granted jump server permissions. | `list(string)` | n/a | yes |
| <a name="input_az_count"></a> [az\_count](#input\_az\_count) | Number of availability zones in a given region. | `number` | n/a | yes |
| <a name="input_cidr"></a> [cidr](#input\_cidr) | The IPv4 CIDR block for the VPC. | `string` | n/a | yes |
| <a name="input_destination_cidr_block"></a> [destination\_cidr\_block](#input\_destination\_cidr\_block) | The CIDR block associated with the local subnet. | `string` | n/a | yes |
| <a name="input_force_destroy"></a> [force\_destroy](#input\_force\_destroy) | Whether deletion protection is active on the module buckets. | `bool` | n/a | yes |
| <a name="input_ssl_port"></a> [ssl\_port](#input\_ssl\_port) | Port for making SSL connections. | `number` | n/a | yes |

## Outputs

No outputs.
<!-- END_TF_DOCS -->