# [ECS Service](https://docs.aws.amazon.com/ecs)

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
| <a name="module_ecs_service_autoscaling_cpu_label"></a> [ecs\_service\_autoscaling\_cpu\_label](#module\_ecs\_service\_autoscaling\_cpu\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_ecs_service_autoscaling_memory_label"></a> [ecs\_service\_autoscaling\_memory\_label](#module\_ecs\_service\_autoscaling\_memory\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_ecs_service_autoscaling_target_label"></a> [ecs\_service\_autoscaling\_target\_label](#module\_ecs\_service\_autoscaling\_target\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_ecs_service_label"></a> [ecs\_service\_label](#module\_ecs\_service\_label) | cloudposse/label/null | 0.25.0 |

## Resources

| Name | Type |
|------|------|
| [aws_appautoscaling_policy.ecs_policy_cpu](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/resources/appautoscaling_policy) | resource |
| [aws_appautoscaling_policy.ecs_policy_memory](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/resources/appautoscaling_policy) | resource |
| [aws_appautoscaling_target.ecs_target](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/resources/appautoscaling_target) | resource |
| [aws_ecs_service.this](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/resources/ecs_service) | resource |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_alb_target_group_arn"></a> [alb\_target\_group\_arn](#input\_alb\_target\_group\_arn) | The ARN of the target group for the ALB. | `string` | n/a | yes |
| <a name="input_assign_public_ip"></a> [assign\_public\_ip](#input\_assign\_public\_ip) | Should the service be exposed. | `bool` | n/a | yes |
| <a name="input_cluster"></a> [cluster](#input\_cluster) | The ARN of the ECS cluster to run the service. | `string` | n/a | yes |
| <a name="input_cluster_name"></a> [cluster\_name](#input\_cluster\_name) | The name of the ECS cluster running the service. | `string` | n/a | yes |
| <a name="input_cpu_scale_in_cooldown"></a> [cpu\_scale\_in\_cooldown](#input\_cpu\_scale\_in\_cooldown) | How long (secs) after a CPU scale-in completes before another can start. | `number` | n/a | yes |
| <a name="input_cpu_scale_out_cooldown"></a> [cpu\_scale\_out\_cooldown](#input\_cpu\_scale\_out\_cooldown) | How long (secs) after a CPU scale-out completes before another can start. | `number` | n/a | yes |
| <a name="input_cpu_target_value"></a> [cpu\_target\_value](#input\_cpu\_target\_value) | Target value for the CPU metric. | `number` | n/a | yes |
| <a name="input_desired_count"></a> [desired\_count](#input\_desired\_count) | Number of ECS services running in parallel. | `number` | n/a | yes |
| <a name="input_environment"></a> [environment](#input\_environment) | Identify the deployment environment. | `string` | n/a | yes |
| <a name="input_force_new_deployment"></a> [force\_new\_deployment](#input\_force\_new\_deployment) | Should an update to the service redeploy task definitions | `bool` | n/a | yes |
| <a name="input_health_check_grace_period"></a> [health\_check\_grace\_period](#input\_health\_check\_grace\_period) | How long to wait before terminating tasks that fail health checks. | `number` | n/a | yes |
| <a name="input_launch_type"></a> [launch\_type](#input\_launch\_type) | What ECS mode the service should run in. | `string` | n/a | yes |
| <a name="input_max_capacity"></a> [max\_capacity](#input\_max\_capacity) | Maximum number for scaling targets. | `number` | n/a | yes |
| <a name="input_max_percent"></a> [max\_percent](#input\_max\_percent) | The upper limit of running tasks in a service during a deployment. | `number` | n/a | yes |
| <a name="input_memory_scale_in_cooldown"></a> [memory\_scale\_in\_cooldown](#input\_memory\_scale\_in\_cooldown) | How long (secs) after a memory scale-in completes before another can start. | `number` | n/a | yes |
| <a name="input_memory_scale_out_cooldown"></a> [memory\_scale\_out\_cooldown](#input\_memory\_scale\_out\_cooldown) | How long (secs) after a memory scale-out completes before another can start. | `number` | n/a | yes |
| <a name="input_memory_target_value"></a> [memory\_target\_value](#input\_memory\_target\_value) | Target value for the memory metric. | `number` | n/a | yes |
| <a name="input_min_capacity"></a> [min\_capacity](#input\_min\_capacity) | Minimum number of scaling targets. | `number` | n/a | yes |
| <a name="input_min_healthy_percent"></a> [min\_healthy\_percent](#input\_min\_healthy\_percent) | The lower limit of running tasks that must remain healthy in a service | `number` | n/a | yes |
| <a name="input_name"></a> [name](#input\_name) | The name of the service. | `string` | n/a | yes |
| <a name="input_namespace"></a> [namespace](#input\_namespace) | The project namespace. | `string` | n/a | yes |
| <a name="input_proxy_name"></a> [proxy\_name](#input\_proxy\_name) | Name of the proxy sidecar container. | `string` | n/a | yes |
| <a name="input_proxy_port"></a> [proxy\_port](#input\_proxy\_port) | Port exposed by the reverse proxy. | `number` | n/a | yes |
| <a name="input_scaling_policy_type"></a> [scaling\_policy\_type](#input\_scaling\_policy\_type) | Which method to use when scaling the cluster. | `string` | n/a | yes |
| <a name="input_scheduling_strategy"></a> [scheduling\_strategy](#input\_scheduling\_strategy) | Scheduling strategy to use for the service. | `string` | n/a | yes |
| <a name="input_security_groups"></a> [security\_groups](#input\_security\_groups) | The security groups mapped to the ECS service. | `list(string)` | n/a | yes |
| <a name="input_service"></a> [service](#input\_service) | An optional service namespace. | `string` | `null` | no |
| <a name="input_subnets"></a> [subnets](#input\_subnets) | The (private) VPC subnets in which to register ECS. | `list(string)` | n/a | yes |
| <a name="input_task_definition"></a> [task\_definition](#input\_task\_definition) | The ARN of the task to run on the service. | `string` | n/a | yes |

## Outputs

No outputs.
<!-- END_TF_DOCS -->