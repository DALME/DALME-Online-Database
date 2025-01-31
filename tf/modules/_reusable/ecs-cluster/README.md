# [ECS Cluster](https://docs.aws.amazon.com/ecs)

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
| <a name="module_ecs_cluster_label"></a> [ecs\_cluster\_label](#module\_ecs\_cluster\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_ecs_cluster_sg_label"></a> [ecs\_cluster\_sg\_label](#module\_ecs\_cluster\_sg\_label) | cloudposse/label/null | 0.25.0 |

## Resources

| Name | Type |
|------|------|
| [aws_ecs_cluster.this](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/resources/ecs_cluster) | resource |
| [aws_ecs_cluster_capacity_providers.this](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/resources/ecs_cluster_capacity_providers) | resource |
| [aws_security_group.ecs](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/resources/security_group) | resource |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_capacity_providers"></a> [capacity\_providers](#input\_capacity\_providers) | Determine where the ECS scaling provisioning comes from. | `list(string)` | n/a | yes |
| <a name="input_default_capacity_provider_strategy"></a> [default\_capacity\_provider\_strategy](#input\_default\_capacity\_provider\_strategy) | Tune the ECS capacity provider strategy | <pre>object({<br>    base              = number,<br>    weight            = number,<br>    capacity_provider = string,<br>  })</pre> | n/a | yes |
| <a name="input_environment"></a> [environment](#input\_environment) | Identify the deployment environment. | `string` | n/a | yes |
| <a name="input_namespace"></a> [namespace](#input\_namespace) | The project namespace. | `string` | n/a | yes |
| <a name="input_service"></a> [service](#input\_service) | An optional service namespace. | `string` | `null` | no |
| <a name="input_vpc_id"></a> [vpc\_id](#input\_vpc\_id) | Identifier for the VPC. | `string` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_arn"></a> [arn](#output\_arn) | The ARN of the ECS cluster. |
| <a name="output_name"></a> [name](#output\_name) | The name of the ecs cluster. |
| <a name="output_security_group_id"></a> [security\_group\_id](#output\_security\_group\_id) | Identify the security group controlling access to the ECS cluster. |
| <a name="output_security_group_label_context"></a> [security\_group\_label\_context](#output\_security\_group\_label\_context) | Label data for the ECS cluster security group. |
<!-- END_TF_DOCS -->