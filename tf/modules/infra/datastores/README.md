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
| <a name="module_postgres"></a> [postgres](#module\_postgres) | ../..//_reusable/rds/ | n/a |

## Resources

| Name | Type |
|------|------|
| [aws_security_group_rule.jump_host_egress_postgres](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/resources/security_group_rule) | resource |
| [aws_security_group_rule.postgres_ingress_jump_host](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/resources/security_group_rule) | resource |
| [aws_kms_alias.global](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/data-sources/kms_alias) | data source |
| [aws_security_group.tunnel](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/data-sources/security_group) | data source |
| [aws_subnets.private](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/data-sources/subnets) | data source |
| [aws_vpc.this](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/data-sources/vpc) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_rds_postgres"></a> [rds\_postgres](#input\_rds\_postgres) | Configuration for a PostgreSQL RDS instance. | <pre>object({<br>    allocated_storage                     = number<br>    apply_immediately                     = bool<br>    backup_retention_period               = number<br>    cidr_blocks                           = string<br>    db_name                               = string<br>    deletion_protection                   = bool<br>    engine                                = string<br>    engine_version                        = number<br>    iam_database_authentication_enabled   = bool<br>    identifier                            = string<br>    instance_class                        = string<br>    ipv6_cidr_blocks                      = string<br>    manage_master_user_password           = bool<br>    multi_az                              = bool<br>    parameter_rds_force_ssl               = bool<br>    performance_insights_enabled          = bool<br>    performance_insights_retention_period = number<br>    port                                  = number<br>    publicly_accessible                   = bool<br>    skip_final_snapshot                   = bool<br>    storage_encrypted                     = bool<br>    storage_type                          = string<br>    username                              = string<br>  })</pre> | n/a | yes |

## Outputs

No outputs.
<!-- END_TF_DOCS -->