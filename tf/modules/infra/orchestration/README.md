# Container Orchestration

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
| <a name="module_ecs_cluster"></a> [ecs\_cluster](#module\_ecs\_cluster) | ../..//_reusable/ecs-cluster/ | n/a |

## Resources

| Name | Type |
|------|------|
| [aws_security_group_rule.ecs_egress](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/resources/security_group_rule) | resource |
| [aws_security_group_rule.ecs_ingress_alb](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/resources/security_group_rule) | resource |
| [aws_security_group_rule.postgres_ingress_ecs](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/resources/security_group_rule) | resource |
| [aws_security_group.alb](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/data-sources/security_group) | data source |
| [aws_security_group.postgres](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/data-sources/security_group) | data source |
| [aws_vpc.this](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/data-sources/vpc) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_capacity_providers"></a> [capacity\_providers](#input\_capacity\_providers) | Determine where the ECS scaling provisioning comes from. | `list(string)` | n/a | yes |
| <a name="input_default_capacity_provider_strategy"></a> [default\_capacity\_provider\_strategy](#input\_default\_capacity\_provider\_strategy) | Tune the ECS capacity provider strategy | <pre>object({<br>    base              = number,<br>    weight            = number,<br>    capacity_provider = string,<br>  })</pre> | n/a | yes |
| <a name="input_postgres_port"></a> [postgres\_port](#input\_postgres\_port) | Port for making PostgreSQL connections. | `number` | n/a | yes |
| <a name="input_proxy_port"></a> [proxy\_port](#input\_proxy\_port) | Reverse proxy listening port. | `number` | n/a | yes |

## Outputs

No outputs.
<!-- END_TF_DOCS -->