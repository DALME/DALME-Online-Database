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
| [aws_db_instance.main](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/db_instance) | resource |
| [aws_db_parameter_group.main](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/db_parameter_group) | resource |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_allocated_storage"></a> [allocated\_storage](#input\_allocated\_storage) | The amount of storage for the db instance. | `number` | n/a | yes |
| <a name="input_backup_retention_period"></a> [backup\_retention\_period](#input\_backup\_retention\_period) | How long to store db backups. | `number` | n/a | yes |
| <a name="input_db_name"></a> [db\_name](#input\_db\_name) | The name of the db db instance. | `string` | n/a | yes |
| <a name="input_db_subnet_group_name"></a> [db\_subnet\_group\_name](#input\_db\_subnet\_group\_name) | The subnet hosting the rds instance. | `string` | n/a | yes |
| <a name="input_deletion_protection"></a> [deletion\_protection](#input\_deletion\_protection) | Whether or not deletion protection is activated for the db instance. | `string` | n/a | yes |
| <a name="input_engine"></a> [engine](#input\_engine) | What type of database is the db instance. | `string` | n/a | yes |
| <a name="input_engine_version"></a> [engine\_version](#input\_engine\_version) | The release version of the db instance. | `number` | n/a | yes |
| <a name="input_environment"></a> [environment](#input\_environment) | Identify the deployment environment. | `string` | n/a | yes |
| <a name="input_identifier"></a> [identifier](#input\_identifier) | Names the rds resource itself. | `string` | n/a | yes |
| <a name="input_instance_class"></a> [instance\_class](#input\_instance\_class) | The RDS db instance type. | `string` | n/a | yes |
| <a name="input_kms_key_arn"></a> [kms\_key\_arn](#input\_kms\_key\_arn) | The project encryption key ARN. | `string` | n/a | yes |
| <a name="input_manage_master_user_password"></a> [manage\_master\_user\_password](#input\_manage\_master\_user\_password) | Toggle automatic password opsec management. | `bool` | n/a | yes |
| <a name="input_multi_az"></a> [multi\_az](#input\_multi\_az) | Is the db replicated across zones for failover. | `bool` | n/a | yes |
| <a name="input_parameter_rds_force_ssl"></a> [parameter\_rds\_force\_ssl](#input\_parameter\_rds\_force\_ssl) | Require SSL to connect to the instance. | `bool` | n/a | yes |
| <a name="input_performance_insights_enabled"></a> [performance\_insights\_enabled](#input\_performance\_insights\_enabled) | Specify whether Performance Insights are enabled. | `bool` | n/a | yes |
| <a name="input_performance_insights_retention_period"></a> [performance\_insights\_retention\_period](#input\_performance\_insights\_retention\_period) | How long to preserve performance logs. | `number` | n/a | yes |
| <a name="input_port"></a> [port](#input\_port) | The bound port of the db instance. | `number` | n/a | yes |
| <a name="input_publicly_accessible"></a> [publicly\_accessible](#input\_publicly\_accessible) | Is db instance access exposed over the internet. | `bool` | n/a | yes |
| <a name="input_service"></a> [service](#input\_service) | The service of the project/stack. | `string` | n/a | yes |
| <a name="input_skip_final_snapshot"></a> [skip\_final\_snapshot](#input\_skip\_final\_snapshot) | Whether to make a final db dump before deletion. | `bool` | n/a | yes |
| <a name="input_storage_encrypted"></a> [storage\_encrypted](#input\_storage\_encrypted) | Is the db instance data encrypted. | `bool` | n/a | yes |
| <a name="input_storage_type"></a> [storage\_type](#input\_storage\_type) | Specify the storage media for the db instance. | `string` | n/a | yes |
| <a name="input_username"></a> [username](#input\_username) | The user accessing the db. | `string` | n/a | yes |
| <a name="input_vpc_security_group_ids"></a> [vpc\_security\_group\_ids](#input\_vpc\_security\_group\_ids) | Identify the RDS security group(s). | `list(string)` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_address"></a> [address](#output\_address) | The address of the RDS instance. |
| <a name="output_master_user_secret_arn"></a> [master\_user\_secret\_arn](#output\_master\_user\_secret\_arn) | The ARN of the db instance password secret. |
| <a name="output_name"></a> [name](#output\_name) | The name of the RDS instance. |
| <a name="output_rds_instance_arn"></a> [rds\_instance\_arn](#output\_rds\_instance\_arn) | The ARN of the RDS instance. |
| <a name="output_username"></a> [username](#output\_username) | The main username of the RDS instance. |
<!-- END_TF_DOCS -->