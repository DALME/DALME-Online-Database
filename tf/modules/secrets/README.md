<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | ~> 1.3 |
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | 5.14.0 |
| <a name="requirement_random"></a> [random](#requirement\_random) | ~> 3.4 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | 5.14.0 |
| <a name="provider_random"></a> [random](#provider\_random) | ~> 3.4 |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [aws_kms_key.main](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/kms_key) | resource |
| [aws_secretsmanager_secret.secrets](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/secretsmanager_secret) | resource |
| [aws_secretsmanager_secret_version.secrets_values](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/secretsmanager_secret_version) | resource |
| [random_password.password](https://registry.terraform.io/providers/hashicorp/random/latest/docs/resources/password) | resource |
| [aws_iam_policy_document.kms](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/data-sources/iam_policy_document) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_account_ids"></a> [account\_ids](#input\_account\_ids) | AWS accounts to be granted KMS key permissions. | `list(string)` | n/a | yes |
| <a name="input_aws_account"></a> [aws\_account](#input\_aws\_account) | The AWS account where resources are created. | `number` | n/a | yes |
| <a name="input_aws_region"></a> [aws\_region](#input\_aws\_region) | The AWS region where resources are created. | `string` | n/a | yes |
| <a name="input_environment"></a> [environment](#input\_environment) | Identify the deployment environment. | `string` | n/a | yes |
| <a name="input_keeper"></a> [keeper](#input\_keeper) | Increment this value to regenerate random secrets. | `number` | n/a | yes |
| <a name="input_recovery_window"></a> [recovery\_window](#input\_recovery\_window) | How many days to preserve deleted secrets before shredding. | `number` | n/a | yes |
| <a name="input_secrets"></a> [secrets](#input\_secrets) | A list of secrets names. | `list(string)` | n/a | yes |
| <a name="input_service"></a> [service](#input\_service) | The service of the project/stack. | `string` | n/a | yes |
| <a name="input_static_secrets"></a> [static\_secrets](#input\_static\_secrets) | Designate secrets that don't change. | `list(string)` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_kms_key_arn"></a> [kms\_key\_arn](#output\_kms\_key\_arn) | ARN for the project KMS encryption key. |
| <a name="output_opensearch_password"></a> [opensearch\_password](#output\_opensearch\_password) | The opensearch master user password. |
| <a name="output_secrets"></a> [secrets](#output\_secrets) | A map of secrets from name to name/value 'Secret' objects. |
| <a name="output_secrets_arns"></a> [secrets\_arns](#output\_secrets\_arns) | AWS identifiers for the registered secrets. |
<!-- END_TF_DOCS -->