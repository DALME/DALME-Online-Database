# [Step Function ECS Scheduled Task](https://aws.amazon.com/step-functions)

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
| <a name="module_sfn_ecs_scheduled_task_event_rule_label"></a> [sfn\_ecs\_scheduled\_task\_event\_rule\_label](#module\_sfn\_ecs\_scheduled\_task\_event\_rule\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_sfn_ecs_scheduled_task_event_target_label"></a> [sfn\_ecs\_scheduled\_task\_event\_target\_label](#module\_sfn\_ecs\_scheduled\_task\_event\_target\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_sfn_ecs_scheduled_task_execution_policy_label"></a> [sfn\_ecs\_scheduled\_task\_execution\_policy\_label](#module\_sfn\_ecs\_scheduled\_task\_execution\_policy\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_sfn_ecs_scheduled_task_execution_role_label"></a> [sfn\_ecs\_scheduled\_task\_execution\_role\_label](#module\_sfn\_ecs\_scheduled\_task\_execution\_role\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_sfn_ecs_scheduled_task_label"></a> [sfn\_ecs\_scheduled\_task\_label](#module\_sfn\_ecs\_scheduled\_task\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_sfn_ecs_scheduled_task_sns_topic_label"></a> [sfn\_ecs\_scheduled\_task\_sns\_topic\_label](#module\_sfn\_ecs\_scheduled\_task\_sns\_topic\_label) | cloudposse/label/null | 0.25.0 |

## Resources

| Name | Type |
|------|------|
| [aws_cloudwatch_event_rule.this](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/resources/cloudwatch_event_rule) | resource |
| [aws_cloudwatch_event_target.publish](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/resources/cloudwatch_event_target) | resource |
| [aws_iam_policy.sfn_execution_policy](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/resources/iam_policy) | resource |
| [aws_iam_role.sfn_execution_role](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/resources/iam_role) | resource |
| [aws_iam_role_policy_attachment.sfn_execution](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/resources/iam_role_policy_attachment) | resource |
| [aws_sfn_state_machine.this](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/resources/sfn_state_machine) | resource |
| [aws_sns_topic.ecs_scheduled_task_failure](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/resources/sns_topic) | resource |
| [aws_sns_topic_subscription.ecs_scheduled_task_failure](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/resources/sns_topic_subscription) | resource |
| [aws_ecs_cluster.this](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/data-sources/ecs_cluster) | data source |
| [aws_iam_policy_document.sfn_execution_policy](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.sfn_role_policy](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/data-sources/iam_policy_document) | data source |
| [aws_kms_alias.global](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/data-sources/kms_alias) | data source |
| [aws_security_group.ecs](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/data-sources/security_group) | data source |
| [aws_subnets.private](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/data-sources/subnets) | data source |
| [aws_vpc.this](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/data-sources/vpc) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_admins"></a> [admins](#input\_admins) | Project admin email addresses. | `list(string)` | n/a | yes |
| <a name="input_assign_public_ip"></a> [assign\_public\_ip](#input\_assign\_public\_ip) | Should the step function be exposed. | `bool` | n/a | yes |
| <a name="input_aws_account"></a> [aws\_account](#input\_aws\_account) | The AWS account where resources are created. | `number` | n/a | yes |
| <a name="input_aws_region"></a> [aws\_region](#input\_aws\_region) | The AWS region where resources are created. | `string` | n/a | yes |
| <a name="input_backoff_rate"></a> [backoff\_rate](#input\_backoff\_rate) | Multiplier that increases the retry interval on each attempt | `number` | n/a | yes |
| <a name="input_container"></a> [container](#input\_container) | The name of the task definition container. | `string` | n/a | yes |
| <a name="input_description"></a> [description](#input\_description) | Information describing the purpose of this step function. | `string` | n/a | yes |
| <a name="input_ecs_task_definition_arn"></a> [ecs\_task\_definition\_arn](#input\_ecs\_task\_definition\_arn) | The ARN of the ECS task definition to be executed. | `string` | n/a | yes |
| <a name="input_ecs_task_execution_role_arn"></a> [ecs\_task\_execution\_role\_arn](#input\_ecs\_task\_execution\_role\_arn) | The ARN of the ECS task execution role. | `string` | n/a | yes |
| <a name="input_ecs_task_role_arn"></a> [ecs\_task\_role\_arn](#input\_ecs\_task\_role\_arn) | The ARN of the ECS task role. | `string` | n/a | yes |
| <a name="input_environment"></a> [environment](#input\_environment) | Identify the deployment environment. | `string` | n/a | yes |
| <a name="input_heartbeat"></a> [heartbeat](#input\_heartbeat) | How long between function 'heartbeats' before timeout (cannot exceed timeout). | `number` | n/a | yes |
| <a name="input_max_attempts"></a> [max\_attempts](#input\_max\_attempts) | Number of times to retry a failed function. | `number` | n/a | yes |
| <a name="input_name"></a> [name](#input\_name) | The name of the scheduled task. | `string` | n/a | yes |
| <a name="input_namespace"></a> [namespace](#input\_namespace) | The project namespace. | `string` | n/a | yes |
| <a name="input_retry_interval"></a> [retry\_interval](#input\_retry\_interval) | How long to wait between function retries. | `number` | n/a | yes |
| <a name="input_schedule_expression"></a> [schedule\_expression](#input\_schedule\_expression) | The expression determining when the rule should run. | `string` | n/a | yes |
| <a name="input_state"></a> [state](#input\_state) | The state of the cloudwatch rule. | `string` | n/a | yes |
| <a name="input_timeout"></a> [timeout](#input\_timeout) | The running time threshold for a function (must exceed heartbeat). | `number` | n/a | yes |

## Outputs

No outputs.
<!-- END_TF_DOCS -->