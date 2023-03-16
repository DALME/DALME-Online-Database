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
| [aws_ecr_lifecycle_policy.images](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/ecr_lifecycle_policy) | resource |
| [aws_ecr_repository.images](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/ecr_repository) | resource |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_force_delete"></a> [force\_delete](#input\_force\_delete) | Whether to activate deletion protection on the repositories. | `bool` | n/a | yes |
| <a name="input_image"></a> [image](#input\_image) | Common container name. | `string` | n/a | yes |
| <a name="input_images"></a> [images](#input\_images) | Application container sub-service names. | `list(string)` | n/a | yes |
| <a name="input_kms_key_arn"></a> [kms\_key\_arn](#input\_kms\_key\_arn) | The project encryption key ARN. | `string` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_repository_arns"></a> [repository\_arns](#output\_repository\_arns) | ARNs for repository containers. |
<!-- END_TF_DOCS -->