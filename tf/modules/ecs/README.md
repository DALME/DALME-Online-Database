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
| [aws_appautoscaling_policy.ecs_policy_cpu](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/appautoscaling_policy) | resource |
| [aws_appautoscaling_policy.ecs_policy_memory](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/appautoscaling_policy) | resource |
| [aws_appautoscaling_target.ecs_target](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/appautoscaling_target) | resource |
| [aws_cloudwatch_event_rule.cleartokens](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/cloudwatch_event_rule) | resource |
| [aws_cloudwatch_event_rule.publish](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/cloudwatch_event_rule) | resource |
| [aws_cloudwatch_event_target.cleartokens](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/cloudwatch_event_target) | resource |
| [aws_cloudwatch_event_target.publish](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/cloudwatch_event_target) | resource |
| [aws_cloudwatch_log_group.proxy_log_group](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/cloudwatch_log_group) | resource |
| [aws_cloudwatch_log_group.web_log_group](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/cloudwatch_log_group) | resource |
| [aws_cloudwatch_log_stream.proxy_log_stream](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/cloudwatch_log_stream) | resource |
| [aws_cloudwatch_log_stream.web_log_stream](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/cloudwatch_log_stream) | resource |
| [aws_ecs_cluster.main](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/ecs_cluster) | resource |
| [aws_ecs_cluster_capacity_providers.main](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/ecs_cluster_capacity_providers) | resource |
| [aws_ecs_service.main](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/ecs_service) | resource |
| [aws_ecs_task_definition.cleartokens](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/ecs_task_definition) | resource |
| [aws_ecs_task_definition.main](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/ecs_task_definition) | resource |
| [aws_ecs_task_definition.publish](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/ecs_task_definition) | resource |
| [aws_iam_policy.cloudwatch_scheduled_task_policy](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/iam_policy) | resource |
| [aws_iam_policy.ecs_task_execution_policy](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/iam_policy) | resource |
| [aws_iam_policy.ecs_task_policy](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/iam_policy) | resource |
| [aws_iam_policy.sfn_execution_policy](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/iam_policy) | resource |
| [aws_iam_role.cloudwatch_scheduled_task_role](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/iam_role) | resource |
| [aws_iam_role.ecs_task_execution_role](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/iam_role) | resource |
| [aws_iam_role.ecs_task_role](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/iam_role) | resource |
| [aws_iam_role.sfn_execution_role](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/iam_role) | resource |
| [aws_iam_role_policy_attachment.cloudwatch_scheduled_task_role](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/iam_role_policy_attachment) | resource |
| [aws_iam_role_policy_attachment.ecs_task_execution_role](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/iam_role_policy_attachment) | resource |
| [aws_iam_role_policy_attachment.ecs_task_role](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/iam_role_policy_attachment) | resource |
| [aws_iam_role_policy_attachment.sfn_execution](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/iam_role_policy_attachment) | resource |
| [aws_sfn_state_machine.cleartokens](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/sfn_state_machine) | resource |
| [aws_sfn_state_machine.publish](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/sfn_state_machine) | resource |
| [aws_sns_topic.ecs_scheduled_task_failure](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/sns_topic) | resource |
| [aws_sns_topic_subscription.ecs_scheduled_task_failure](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/sns_topic_subscription) | resource |
| [aws_iam_policy_document.cloudwatch_scheduled_task_policy](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.cloudwatch_scheduled_task_role](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.ecs_task_execution_policy](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.ecs_task_execution_role](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.ecs_task_policy](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.ecs_task_role](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.sfn_execution_policy](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.sfn_role_policy](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/data-sources/iam_policy_document) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_admins"></a> [admins](#input\_admins) | Project admin email addresses. | `list(string)` | n/a | yes |
| <a name="input_alb_target_group_arn"></a> [alb\_target\_group\_arn](#input\_alb\_target\_group\_arn) | The ARN of the target group for the ALB. | `string` | n/a | yes |
| <a name="input_allowed_hosts"></a> [allowed\_hosts](#input\_allowed\_hosts) | Permitted domains for requests. | `list(string)` | n/a | yes |
| <a name="input_aws_account"></a> [aws\_account](#input\_aws\_account) | The AWS account where resources are created. | `number` | n/a | yes |
| <a name="input_aws_region"></a> [aws\_region](#input\_aws\_region) | The AWS region where resources are created. | `string` | n/a | yes |
| <a name="input_capacity_provider"></a> [capacity\_provider](#input\_capacity\_provider) | Determine where ECS scaling provisioning comes from. | `string` | n/a | yes |
| <a name="input_cloudfront_arn"></a> [cloudfront\_arn](#input\_cloudfront\_arn) | ARN for the cloudfront distribution. | `string` | n/a | yes |
| <a name="input_cloudfront_domain"></a> [cloudfront\_domain](#input\_cloudfront\_domain) | Pass the cloudfront endpoint for injection in the tasks. | `string` | n/a | yes |
| <a name="input_cpu_scale_in_cooldown"></a> [cpu\_scale\_in\_cooldown](#input\_cpu\_scale\_in\_cooldown) | How long (secs) after a CPU scale-in completes before another can start. | `number` | n/a | yes |
| <a name="input_cpu_scale_out_cooldown"></a> [cpu\_scale\_out\_cooldown](#input\_cpu\_scale\_out\_cooldown) | How long (secs) after a CPU scale-out completes before another can start. | `number` | n/a | yes |
| <a name="input_cpu_target_value"></a> [cpu\_target\_value](#input\_cpu\_target\_value) | Target value for the CPU metric. | `number` | n/a | yes |
| <a name="input_db_host"></a> [db\_host](#input\_db\_host) | The host of the db instance. | `string` | n/a | yes |
| <a name="input_db_name"></a> [db\_name](#input\_db\_name) | The name of the db instance. | `string` | n/a | yes |
| <a name="input_ecs_security_groups"></a> [ecs\_security\_groups](#input\_ecs\_security\_groups) | The security groups mapped to the ECS service. | `list(string)` | n/a | yes |
| <a name="input_environment"></a> [environment](#input\_environment) | Identify the deployment environment. | `string` | n/a | yes |
| <a name="input_fargate_cpu"></a> [fargate\_cpu](#input\_fargate\_cpu) | Fargate instance CPU units to provision (1 vCPU = 1024 CPU units). | `number` | n/a | yes |
| <a name="input_fargate_memory"></a> [fargate\_memory](#input\_fargate\_memory) | Fargate instance memory to provision (in MiB). | `number` | n/a | yes |
| <a name="input_gunicorn_config"></a> [gunicorn\_config](#input\_gunicorn\_config) | Path to the gunicorn config file. | `string` | n/a | yes |
| <a name="input_health_check_grace_period"></a> [health\_check\_grace\_period](#input\_health\_check\_grace\_period) | How long to wait before terminating tasks that fail health checks. | `number` | n/a | yes |
| <a name="input_image"></a> [image](#input\_image) | Common container name. | `string` | n/a | yes |
| <a name="input_kms_key_arn"></a> [kms\_key\_arn](#input\_kms\_key\_arn) | The project encryption key ARN. | `string` | n/a | yes |
| <a name="input_log_level"></a> [log\_level](#input\_log\_level) | Set the severity of the web logger. | `string` | n/a | yes |
| <a name="input_log_retention_in_days"></a> [log\_retention\_in\_days](#input\_log\_retention\_in\_days) | How long to keep cloudwatch records. | `number` | n/a | yes |
| <a name="input_max_capacity"></a> [max\_capacity](#input\_max\_capacity) | Maximum number for scaling targets. | `number` | n/a | yes |
| <a name="input_max_percent"></a> [max\_percent](#input\_max\_percent) | The upper limit of running tasks in a service during a deployment. | `number` | n/a | yes |
| <a name="input_memory_scale_in_cooldown"></a> [memory\_scale\_in\_cooldown](#input\_memory\_scale\_in\_cooldown) | How long (secs) after a memory scale-in completes before another can start. | `number` | n/a | yes |
| <a name="input_memory_scale_out_cooldown"></a> [memory\_scale\_out\_cooldown](#input\_memory\_scale\_out\_cooldown) | How long (secs) after a memory scale-out completes before another can start. | `number` | n/a | yes |
| <a name="input_memory_target_value"></a> [memory\_target\_value](#input\_memory\_target\_value) | Target value for the memory metric. | `number` | n/a | yes |
| <a name="input_min_capacity"></a> [min\_capacity](#input\_min\_capacity) | Minimum number of scaling targets. | `number` | n/a | yes |
| <a name="input_min_healthy_percent"></a> [min\_healthy\_percent](#input\_min\_healthy\_percent) | The lower limit of running tasks that must remain healthy in a service | `number` | n/a | yes |
| <a name="input_oauth_client_id"></a> [oauth\_client\_id](#input\_oauth\_client\_id) | Public identifier for the OAuth application. | `string` | n/a | yes |
| <a name="input_opensearch_endpoint"></a> [opensearch\_endpoint](#input\_opensearch\_endpoint) | Domain-specific endpoint to submit OpenSearch requests. | `string` | n/a | yes |
| <a name="input_opensearch_username"></a> [opensearch\_username](#input\_opensearch\_username) | Login username for the OpenSearch service.. | `string` | n/a | yes |
| <a name="input_postgres_password_secret_arn"></a> [postgres\_password\_secret\_arn](#input\_postgres\_password\_secret\_arn) | The ARN of the self-managed postgres password secret. | `string` | n/a | yes |
| <a name="input_proxy_port"></a> [proxy\_port](#input\_proxy\_port) | Port exposed by the reverse proxy. | `number` | n/a | yes |
| <a name="input_registry"></a> [registry](#input\_registry) | The ECR registry containing task images. | `string` | n/a | yes |
| <a name="input_repository_arns"></a> [repository\_arns](#input\_repository\_arns) | Identifers for the container repositories. | `list(string)` | n/a | yes |
| <a name="input_scaling_policy_type"></a> [scaling\_policy\_type](#input\_scaling\_policy\_type) | Which method to use when scaling the cluster. | `string` | n/a | yes |
| <a name="input_scheduled_tasks"></a> [scheduled\_tasks](#input\_scheduled\_tasks) | Data for scheduled tasks. | <pre>object({<br>    cleartokens = object({<br>      assign_public_ip    = bool,<br>      is_enabled          = bool,<br>      schedule_expression = string,<br>    }),<br>    publish = object({<br>      assign_public_ip    = bool,<br>      is_enabled          = bool,<br>      schedule_expression = string,<br>    }),<br>  })</pre> | n/a | yes |
| <a name="input_secrets"></a> [secrets](#input\_secrets) | A list of secrets as name/valueFrom 'Secret' objects. | `map(map(string))` | n/a | yes |
| <a name="input_secrets_arns"></a> [secrets\_arns](#input\_secrets\_arns) | Identifers for managed secrets. | `list(string)` | n/a | yes |
| <a name="input_service"></a> [service](#input\_service) | The service of the project/stack. | `string` | n/a | yes |
| <a name="input_service_desired_count"></a> [service\_desired\_count](#input\_service\_desired\_count) | Number of ECS services running in parallel. | `number` | n/a | yes |
| <a name="input_sfn_backoff_rate"></a> [sfn\_backoff\_rate](#input\_sfn\_backoff\_rate) | Multiplier that increases the retry interval on each attempt | `number` | n/a | yes |
| <a name="input_sfn_heartbeat"></a> [sfn\_heartbeat](#input\_sfn\_heartbeat) | How long between function 'heartbeats' before timeout (cannot exceed timeout). | `number` | n/a | yes |
| <a name="input_sfn_max_attempts"></a> [sfn\_max\_attempts](#input\_sfn\_max\_attempts) | Number of times to retry a failed function. | `number` | n/a | yes |
| <a name="input_sfn_retry_interval"></a> [sfn\_retry\_interval](#input\_sfn\_retry\_interval) | How long to wait between function retries. | `number` | n/a | yes |
| <a name="input_sfn_timeout"></a> [sfn\_timeout](#input\_sfn\_timeout) | The running time threshold for a function (must exceed heartbeat). | `number` | n/a | yes |
| <a name="input_staticfiles_arn"></a> [staticfiles\_arn](#input\_staticfiles\_arn) | Identifer for the static assets bucket. | `string` | n/a | yes |
| <a name="input_staticfiles_bucket"></a> [staticfiles\_bucket](#input\_staticfiles\_bucket) | The name of the s3 bucket containing staticfiles. | `string` | n/a | yes |
| <a name="input_subnets"></a> [subnets](#input\_subnets) | The (private) VPC subnets in which to register ECS. | `list(string)` | n/a | yes |
| <a name="input_tenant_domains"></a> [tenant\_domains](#input\_tenant\_domains) | The origin(s) of the service. | `set(string)` | n/a | yes |
| <a name="input_threads"></a> [threads](#input\_threads) | Number of gunicorn threads. | `number` | n/a | yes |
| <a name="input_web_port"></a> [web\_port](#input\_web\_port) | The port exposed by the task container. | `number` | n/a | yes |
| <a name="input_worker"></a> [worker](#input\_worker) | The gunicorn worker type. | `string` | n/a | yes |
| <a name="input_worker_tmp"></a> [worker\_tmp](#input\_worker\_tmp) | The gunicorn worker tmp directory. | `string` | n/a | yes |
| <a name="input_workers"></a> [workers](#input\_workers) | How many gunicorn workers to spawn. | `number` | n/a | yes |
| <a name="input_wsgi"></a> [wsgi](#input\_wsgi) | The entrypoint of the wsgi application. | `string` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_ecs_cluster"></a> [ecs\_cluster](#output\_ecs\_cluster) | The name of the ecs cluster. |
| <a name="output_ecs_service"></a> [ecs\_service](#output\_ecs\_service) | The name of the ecs service. |
<!-- END_TF_DOCS -->