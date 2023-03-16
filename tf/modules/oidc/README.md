<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | ~> 1.3 |
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | 5.14.0 |
| <a name="requirement_tls"></a> [tls](#requirement\_tls) | 4.0.4 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | 5.14.0 |
| <a name="provider_tls"></a> [tls](#provider\_tls) | 4.0.4 |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [aws_iam_openid_connect_provider.github](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/iam_openid_connect_provider) | resource |
| [aws_iam_policy.gha_oidc_policy](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/iam_policy) | resource |
| [aws_iam_role.gha_oidc_role](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/iam_role) | resource |
| [aws_iam_role_policy_attachment.ecs_full_access_policy_attachment](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/iam_role_policy_attachment) | resource |
| [aws_iam_role_policy_attachment.gha_oidc_role](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/iam_role_policy_attachment) | resource |
| [aws_iam_policy_document.gha_oidc_policy](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.gha_oidc_role](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/data-sources/iam_policy_document) | data source |
| [tls_certificate.github](https://registry.terraform.io/providers/hashicorp/tls/4.0.4/docs/data-sources/certificate) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_aws_account"></a> [aws\_account](#input\_aws\_account) | The AWS account where resources are created. | `number` | n/a | yes |
| <a name="input_aws_region"></a> [aws\_region](#input\_aws\_region) | The AWS region where resources are created. | `string` | n/a | yes |
| <a name="input_environment"></a> [environment](#input\_environment) | Identify the deployment environment. | `string` | n/a | yes |
| <a name="input_gha_oidc_role_name"></a> [gha\_oidc\_role\_name](#input\_gha\_oidc\_role\_name) | Name of the github action OIDC role. | `string` | n/a | yes |
| <a name="input_lock_table"></a> [lock\_table](#input\_lock\_table) | DynamoDB table holding terraform state locks. | `string` | n/a | yes |
| <a name="input_oidc_allowed"></a> [oidc\_allowed](#input\_oidc\_allowed) | Github repos/branches allowed to assume to OIDC role. | `list(map(string))` | n/a | yes |
| <a name="input_service"></a> [service](#input\_service) | The service of the project/stack. | `string` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_gha_oidc_role_name"></a> [gha\_oidc\_role\_name](#output\_gha\_oidc\_role\_name) | The name of the Github Actions OIDC role. |
| <a name="output_oidc_provider_arn"></a> [oidc\_provider\_arn](#output\_oidc\_provider\_arn) | ARN for the github OIDC connection/fingerprint. |
<!-- END_TF_DOCS -->