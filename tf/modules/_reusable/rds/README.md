[RDS](https://aws.amazon.com/rds/)

<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | ~> 1.14.0 |
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | 6.25.0 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | 6.25.0 |

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_rds_label"></a> [rds\_label](#module\_rds\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_rds_pg_label"></a> [rds\_pg\_label](#module\_rds\_pg\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_rds_sbng_label"></a> [rds\_sbng\_label](#module\_rds\_sbng\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_rds_sg_label"></a> [rds\_sg\_label](#module\_rds\_sg\_label) | cloudposse/label/null | 0.25.0 |

## Resources

| Name | Type |
|------|------|
| [aws_db_instance.this](https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/db_instance) | resource |
| [aws_db_parameter_group.this](https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/db_parameter_group) | resource |
| [aws_db_subnet_group.this](https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/db_subnet_group) | resource |
| [aws_security_group.this](https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/security_group) | resource |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_allocated_storage"></a> [allocated\_storage](#input\_allocated\_storage) | The amount of storage for the db instance. | `number` | n/a | yes |
| <a name="input_apply_immediately"></a> [apply\_immediately](#input\_apply\_immediately) | Apply modification to the instance immediately or wait until the next maintenance window. | `bool` | n/a | yes |
| <a name="input_backup_retention_period"></a> [backup\_retention\_period](#input\_backup\_retention\_period) | How long to store db backups. | `number` | n/a | yes |
| <a name="input_db_name"></a> [db\_name](#input\_db\_name) | The name of the db instance. | `string` | n/a | yes |
| <a name="input_deletion_protection"></a> [deletion\_protection](#input\_deletion\_protection) | Whether or not deletion protection is activated for the db instance. | `string` | n/a | yes |
| <a name="input_engine"></a> [engine](#input\_engine) | What type of database is the db instance. | `string` | n/a | yes |
| <a name="input_engine_version"></a> [engine\_version](#input\_engine\_version) | The release version of the db instance. | `number` | n/a | yes |
| <a name="input_environment"></a> [environment](#input\_environment) | Identify the deployment environment. | `string` | n/a | yes |
| <a name="input_iam_database_authentication_enabled"></a> [iam\_database\_authentication\_enabled](#input\_iam\_database\_authentication\_enabled) | Allow db connections via IAM. | `bool` | n/a | yes |
| <a name="input_identifier"></a> [identifier](#input\_identifier) | Names the rds resource itself. | `string` | n/a | yes |
| <a name="input_instance_class"></a> [instance\_class](#input\_instance\_class) | The RDS db instance type. | `string` | n/a | yes |
| <a name="input_kms_key_arn"></a> [kms\_key\_arn](#input\_kms\_key\_arn) | The encryption key ARN. | `string` | n/a | yes |
| <a name="input_manage_master_user_password"></a> [manage\_master\_user\_password](#input\_manage\_master\_user\_password) | Toggle automatic password opsec management. | `bool` | n/a | yes |
| <a name="input_multi_az"></a> [multi\_az](#input\_multi\_az) | Is the db replicated across zones for failover. | `bool` | n/a | yes |
| <a name="input_namespace"></a> [namespace](#input\_namespace) | The project namespace. | `string` | n/a | yes |
| <a name="input_parameter_rds_force_ssl"></a> [parameter\_rds\_force\_ssl](#input\_parameter\_rds\_force\_ssl) | Require SSL to connect to the instance. | `bool` | n/a | yes |
| <a name="input_performance_insights_enabled"></a> [performance\_insights\_enabled](#input\_performance\_insights\_enabled) | Specify whether Performance Insights are enabled. | `bool` | n/a | yes |
| <a name="input_performance_insights_retention_period"></a> [performance\_insights\_retention\_period](#input\_performance\_insights\_retention\_period) | How long to preserve performance logs. | `number` | n/a | yes |
| <a name="input_port"></a> [port](#input\_port) | The bound port of the db instance. | `number` | n/a | yes |
| <a name="input_publicly_accessible"></a> [publicly\_accessible](#input\_publicly\_accessible) | Is db instance access exposed over the internet. | `bool` | n/a | yes |
| <a name="input_service"></a> [service](#input\_service) | An optional service namespace. | `string` | `null` | no |
| <a name="input_skip_final_snapshot"></a> [skip\_final\_snapshot](#input\_skip\_final\_snapshot) | Whether to make a final db dump before deletion. | `bool` | n/a | yes |
| <a name="input_storage_encrypted"></a> [storage\_encrypted](#input\_storage\_encrypted) | Is the db instance data encrypted. | `bool` | n/a | yes |
| <a name="input_storage_type"></a> [storage\_type](#input\_storage\_type) | Specify the storage media for the db instance. | `string` | n/a | yes |
| <a name="input_subnet_ids"></a> [subnet\_ids](#input\_subnet\_ids) | Private subnets of the VPC for the instance to occupy. | `list(any)` | n/a | yes |
| <a name="input_username"></a> [username](#input\_username) | The user accessing the db. | `string` | n/a | yes |
| <a name="input_vpc_id"></a> [vpc\_id](#input\_vpc\_id) | Identifier for the VPC. | `string` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_security_group_id"></a> [security\_group\_id](#output\_security\_group\_id) | Identifier for the RDS instance's security group. |
| <a name="output_security_group_label_context"></a> [security\_group\_label\_context](#output\_security\_group\_label\_context) | Label data for the RDS instance's security group. |
<!-- END_TF_DOCS -->