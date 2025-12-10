# [OIDC](https://registry.terraform.io/modules/terraform-module/github-oidc-provider/aws/latest)

Deploys a Github Actions OIDC provider to your environment.

<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | ~> 1.14.0 |
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | 6.25.0 |
| <a name="requirement_tls"></a> [tls](#requirement\_tls) | 4.1.0 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | 6.25.0 |
| <a name="provider_tls"></a> [tls](#provider\_tls) | 4.1.0 |

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_oidc_label"></a> [oidc\_label](#module\_oidc\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_oidc_role_label"></a> [oidc\_role\_label](#module\_oidc\_role\_label) | cloudposse/label/null | 0.25.0 |

## Resources

| Name | Type |
|------|------|
| [aws_iam_openid_connect_provider.github](https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/iam_openid_connect_provider) | resource |
| [aws_iam_role.this](https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/iam_role) | resource |
| [aws_iam_policy_document.this](https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/data-sources/iam_policy_document) | data source |
| [tls_certificate.github](https://registry.terraform.io/providers/hashicorp/tls/4.1.0/docs/data-sources/certificate) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_allowed"></a> [allowed](#input\_allowed) | Github org/repos/branches allowed to assume to OIDC role. | `list(map(string))` | n/a | yes |
| <a name="input_environment"></a> [environment](#input\_environment) | Identify the deployment environment. | `string` | n/a | yes |
| <a name="input_namespace"></a> [namespace](#input\_namespace) | The project namespace. | `string` | n/a | yes |
| <a name="input_provider_name"></a> [provider\_name](#input\_provider\_name) | Name of the github action OIDC provider resource. | `string` | n/a | yes |
| <a name="input_role_name"></a> [role\_name](#input\_role\_name) | Name of the github action OIDC role. | `string` | n/a | yes |
| <a name="input_service"></a> [service](#input\_service) | An optional service namespace. | `string` | `null` | no |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_provider_arn"></a> [provider\_arn](#output\_provider\_arn) | The ARN of the github OIDC provider resource. |
| <a name="output_role_name"></a> [role\_name](#output\_role\_name) | The full name of the Github Actions OIDC role. |
<!-- END_TF_DOCS -->