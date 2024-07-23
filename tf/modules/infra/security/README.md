Security

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
| <a name="module_kms_label"></a> [kms\_label](#module\_kms\_label) | cloudposse/label/null | 0.25.0 |

## Resources

| Name | Type |
|------|------|
| [aws_kms_alias.global](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/resources/kms_alias) | resource |
| [aws_kms_key.global](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/resources/kms_key) | resource |
| [aws_iam_policy_document.kms](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/data-sources/iam_policy_document) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_allowed_roles"></a> [allowed\_roles](#input\_allowed\_roles) | AWS assumed roles to be granted KMS key permissions. | `list(string)` | n/a | yes |

## Outputs

No outputs.
<!-- END_TF_DOCS -->