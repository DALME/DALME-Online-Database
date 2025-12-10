# Authorization

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
| <a name="module_oidc"></a> [oidc](#module\_oidc) | ../..//_reusable/oidc/ | n/a |
| <a name="module_oidc_policy"></a> [oidc\_policy](#module\_oidc\_policy) | cloudposse/label/null | 0.25.0 |
| <a name="module_oidc_policy_one"></a> [oidc\_policy\_one](#module\_oidc\_policy\_one) | cloudposse/label/null | 0.25.0 |
| <a name="module_oidc_policy_two"></a> [oidc\_policy\_two](#module\_oidc\_policy\_two) | cloudposse/label/null | 0.25.0 |

## Resources

| Name | Type |
|------|------|
| [aws_iam_policy.gha_oidc_policy_one](https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/iam_policy) | resource |
| [aws_iam_policy.gha_oidc_policy_two](https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/iam_policy) | resource |
| [aws_iam_role_policy_attachment.ecs_full_access_policy_attachment](https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/iam_role_policy_attachment) | resource |
| [aws_iam_role_policy_attachment.gha_oidc_role_one](https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/iam_role_policy_attachment) | resource |
| [aws_iam_role_policy_attachment.gha_oidc_role_two](https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/iam_role_policy_attachment) | resource |
| [aws_iam_policy_document.gha_oidc_policy_one](https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.gha_oidc_policy_two](https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/data-sources/iam_policy_document) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_allowed_oidc"></a> [allowed\_oidc](#input\_allowed\_oidc) | Github repos/branches allowed to assume to OIDC role. | `list(map(string))` | n/a | yes |
| <a name="input_lock_table"></a> [lock\_table](#input\_lock\_table) | DynamoDB table holding terraform state locks. | `string` | n/a | yes |

## Outputs

No outputs.
<!-- END_TF_DOCS -->