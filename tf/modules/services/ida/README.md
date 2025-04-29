# IDA

<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | ~> 1.6 |
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | 5.70.0 |
| <a name="requirement_external"></a> [external](#requirement\_external) | 2.3.4 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | 5.70.0 |
| <a name="provider_external"></a> [external](#provider\_external) | 2.3.4 |

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_ecr"></a> [ecr](#module\_ecr) | ../..//_reusable/ecr/ | n/a |
| <a name="module_ecs_service"></a> [ecs\_service](#module\_ecs\_service) | ../..//_reusable/ecs-service/ | n/a |
| <a name="module_ida_ecs_task_definition_label"></a> [ida\_ecs\_task\_definition\_label](#module\_ida\_ecs\_task\_definition\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_ida_ecs_task_execution_label"></a> [ida\_ecs\_task\_execution\_label](#module\_ida\_ecs\_task\_execution\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_ida_ecs_task_execution_policy_label"></a> [ida\_ecs\_task\_execution\_policy\_label](#module\_ida\_ecs\_task\_execution\_policy\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_ida_ecs_task_execution_role_label"></a> [ida\_ecs\_task\_execution\_role\_label](#module\_ida\_ecs\_task\_execution\_role\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_ida_ecs_task_label"></a> [ida\_ecs\_task\_label](#module\_ida\_ecs\_task\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_ida_ecs_task_policy_label"></a> [ida\_ecs\_task\_policy\_label](#module\_ida\_ecs\_task\_policy\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_ida_ecs_task_role_label"></a> [ida\_ecs\_task\_role\_label](#module\_ida\_ecs\_task\_role\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_ida_label"></a> [ida\_label](#module\_ida\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_ida_log_group_app_label"></a> [ida\_log\_group\_app\_label](#module\_ida\_log\_group\_app\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_ida_log_group_label"></a> [ida\_log\_group\_label](#module\_ida\_log\_group\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_ida_log_group_proxy_label"></a> [ida\_log\_group\_proxy\_label](#module\_ida\_log\_group\_proxy\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_ida_log_label"></a> [ida\_log\_label](#module\_ida\_log\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_ida_log_stream_app_label"></a> [ida\_log\_stream\_app\_label](#module\_ida\_log\_stream\_app\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_ida_log_stream_label"></a> [ida\_log\_stream\_label](#module\_ida\_log\_stream\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_ida_log_stream_proxy_label"></a> [ida\_log\_stream\_proxy\_label](#module\_ida\_log\_stream\_proxy\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_ida_sfn_ecs_scheduled_task_cleartokens_label"></a> [ida\_sfn\_ecs\_scheduled\_task\_cleartokens\_label](#module\_ida\_sfn\_ecs\_scheduled\_task\_cleartokens\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_ida_sfn_ecs_scheduled_task_label"></a> [ida\_sfn\_ecs\_scheduled\_task\_label](#module\_ida\_sfn\_ecs\_scheduled\_task\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_ida_sfn_ecs_scheduled_task_publish_label"></a> [ida\_sfn\_ecs\_scheduled\_task\_publish\_label](#module\_ida\_sfn\_ecs\_scheduled\_task\_publish\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_ida_sns_ecs_scheduled_task_failure_label"></a> [ida\_sns\_ecs\_scheduled\_task\_failure\_label](#module\_ida\_sns\_ecs\_scheduled\_task\_failure\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_secret"></a> [secret](#module\_secret) | ../..//_reusable/secret/ | n/a |
| <a name="module_sfn_cleartokens"></a> [sfn\_cleartokens](#module\_sfn\_cleartokens) | ../..//_reusable/sfn-ecs-scheduled-task/ | n/a |
| <a name="module_sfn_publish"></a> [sfn\_publish](#module\_sfn\_publish) | ../..//_reusable/sfn-ecs-scheduled-task/ | n/a |

## Resources

| Name | Type |
|------|------|
| [aws_cloudwatch_log_group.app_log_group](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/resources/cloudwatch_log_group) | resource |
| [aws_cloudwatch_log_group.proxy_log_group](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/resources/cloudwatch_log_group) | resource |
| [aws_cloudwatch_log_stream.app_log_stream](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/resources/cloudwatch_log_stream) | resource |
| [aws_cloudwatch_log_stream.proxy_log_stream](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/resources/cloudwatch_log_stream) | resource |
| [aws_ecs_task_definition.cleartokens](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/resources/ecs_task_definition) | resource |
| [aws_ecs_task_definition.publish](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/resources/ecs_task_definition) | resource |
| [aws_ecs_task_definition.this](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/resources/ecs_task_definition) | resource |
| [aws_iam_policy.ecs_task_execution_policy](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/resources/iam_policy) | resource |
| [aws_iam_policy.ecs_task_policy](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/resources/iam_policy) | resource |
| [aws_iam_role.ecs_task_execution_role](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/resources/iam_role) | resource |
| [aws_iam_role.ecs_task_role](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/resources/iam_role) | resource |
| [aws_iam_role_policy_attachment.ecs_task_execution_role](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/resources/iam_role_policy_attachment) | resource |
| [aws_iam_role_policy_attachment.ecs_task_role](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/resources/iam_role_policy_attachment) | resource |
| [aws_sns_topic.ecs_scheduled_task_failure](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/resources/sns_topic) | resource |
| [aws_sns_topic_subscription.ecs_scheduled_task_failure](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/resources/sns_topic_subscription) | resource |
| [aws_db_instance.postgres](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/data-sources/db_instance) | data source |
| [aws_ecs_cluster.this](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/data-sources/ecs_cluster) | data source |
| [aws_iam_policy_document.ecs_task_execution_policy](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.ecs_task_execution_role](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.ecs_task_policy](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.ecs_task_role](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/data-sources/iam_policy_document) | data source |
| [aws_kms_alias.global](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/data-sources/kms_alias) | data source |
| [aws_lb_target_group.this](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/data-sources/lb_target_group) | data source |
| [aws_opensearch_domain.this](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/data-sources/opensearch_domain) | data source |
| [aws_s3_bucket.staticfiles](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/data-sources/s3_bucket) | data source |
| [aws_secretsmanager_secret_version.dam](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/data-sources/secretsmanager_secret_version) | data source |
| [aws_secretsmanager_secret_version.oidc_rsa_key](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/data-sources/secretsmanager_secret_version) | data source |
| [aws_secretsmanager_secret_version.opensearch_master_user](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/data-sources/secretsmanager_secret_version) | data source |
| [aws_secretsmanager_secret_version.plausible](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/data-sources/secretsmanager_secret_version) | data source |
| [aws_secretsmanager_secret_version.zotero](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/data-sources/secretsmanager_secret_version) | data source |
| [aws_security_group.ecs](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/data-sources/security_group) | data source |
| [aws_subnets.private](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/data-sources/subnets) | data source |
| [aws_vpc.this](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/data-sources/vpc) | data source |
| [external_external.cloudfront](https://registry.terraform.io/providers/hashicorp/external/2.3.4/docs/data-sources/external) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_admins"></a> [admins](#input\_admins) | Project admin email addresses. | `list(string)` | n/a | yes |
| <a name="input_allowed_hosts"></a> [allowed\_hosts](#input\_allowed\_hosts) | Permitted domains for requests. | `list(string)` | n/a | yes |
| <a name="input_app_port"></a> [app\_port](#input\_app\_port) | The port exposed by the app container. | `number` | n/a | yes |
| <a name="input_assign_public_ip"></a> [assign\_public\_ip](#input\_assign\_public\_ip) | Should the service be exposed. | `bool` | n/a | yes |
| <a name="input_cpu_scale_in_cooldown"></a> [cpu\_scale\_in\_cooldown](#input\_cpu\_scale\_in\_cooldown) | How long (secs) after a CPU scale-in completes before another can start. | `number` | n/a | yes |
| <a name="input_cpu_scale_out_cooldown"></a> [cpu\_scale\_out\_cooldown](#input\_cpu\_scale\_out\_cooldown) | How long (secs) after a CPU scale-out completes before another can start. | `number` | n/a | yes |
| <a name="input_cpu_target_value"></a> [cpu\_target\_value](#input\_cpu\_target\_value) | Target value for the CPU metric. | `number` | n/a | yes |
| <a name="input_domain"></a> [domain](#input\_domain) | The origin of the service. | `string` | n/a | yes |
| <a name="input_fargate_cpu"></a> [fargate\_cpu](#input\_fargate\_cpu) | Fargate instance CPU units to provision (1 vCPU = 1024 CPU units). | `number` | n/a | yes |
| <a name="input_fargate_memory"></a> [fargate\_memory](#input\_fargate\_memory) | Fargate instance memory to provision (in MiB). | `number` | n/a | yes |
| <a name="input_force_delete"></a> [force\_delete](#input\_force\_delete) | Activate deletion protection on this service's ECR repositories. | `bool` | n/a | yes |
| <a name="input_force_new_deployment"></a> [force\_new\_deployment](#input\_force\_new\_deployment) | Should an update to the service redeploy task definitions | `bool` | n/a | yes |
| <a name="input_gunicorn_config"></a> [gunicorn\_config](#input\_gunicorn\_config) | Path to the gunicorn config file. | `string` | n/a | yes |
| <a name="input_health_check_grace_period"></a> [health\_check\_grace\_period](#input\_health\_check\_grace\_period) | How long to wait before terminating tasks that fail health checks. | `number` | n/a | yes |
| <a name="input_images"></a> [images](#input\_images) | Container repository names for this service. | `list(string)` | n/a | yes |
| <a name="input_keepers"></a> [keepers](#input\_keepers) | Arbitrary key/value pairs that force secret regeneration on change. | <pre>object({<br>    admin_user_version          = number<br>    django_secret_key_version   = number<br>    oauth_client_secret_version = number<br>  })</pre> | n/a | yes |
| <a name="input_launch_type"></a> [launch\_type](#input\_launch\_type) | What ECS mode the service should run in. | `string` | n/a | yes |
| <a name="input_log_level"></a> [log\_level](#input\_log\_level) | Set the severity of the app logger. | `string` | n/a | yes |
| <a name="input_log_retention_in_days"></a> [log\_retention\_in\_days](#input\_log\_retention\_in\_days) | How long to keep cloudwatch records. | `number` | n/a | yes |
| <a name="input_max_capacity"></a> [max\_capacity](#input\_max\_capacity) | Maximum number for scaling targets. | `number` | n/a | yes |
| <a name="input_max_percent"></a> [max\_percent](#input\_max\_percent) | The upper limit of running tasks in a service during a deployment. | `number` | n/a | yes |
| <a name="input_memory_scale_in_cooldown"></a> [memory\_scale\_in\_cooldown](#input\_memory\_scale\_in\_cooldown) | How long (secs) after a memory scale-in completes before another can start. | `number` | n/a | yes |
| <a name="input_memory_scale_out_cooldown"></a> [memory\_scale\_out\_cooldown](#input\_memory\_scale\_out\_cooldown) | How long (secs) after a memory scale-out completes before another can start. | `number` | n/a | yes |
| <a name="input_memory_target_value"></a> [memory\_target\_value](#input\_memory\_target\_value) | Target value for the memory metric. | `number` | n/a | yes |
| <a name="input_min_capacity"></a> [min\_capacity](#input\_min\_capacity) | Minimum number of scaling targets. | `number` | n/a | yes |
| <a name="input_min_healthy_percent"></a> [min\_healthy\_percent](#input\_min\_healthy\_percent) | The lower limit of running tasks that must remain healthy in a service | `number` | n/a | yes |
| <a name="input_oauth_client_id"></a> [oauth\_client\_id](#input\_oauth\_client\_id) | Identifier for the OAuth 2.0 client. | `string` | n/a | yes |
| <a name="input_opensearch_master_user_secret_name"></a> [opensearch\_master\_user\_secret\_name](#input\_opensearch\_master\_user\_secret\_name) | Identifies the Opensearch master user secret. | `string` | n/a | yes |
| <a name="input_postgres_version"></a> [postgres\_version](#input\_postgres\_version) | The release version of the rds postgres instance. | `number` | n/a | yes |
| <a name="input_proxy_port"></a> [proxy\_port](#input\_proxy\_port) | Port exposed by the reverse proxy. | `number` | n/a | yes |
| <a name="input_recovery_window"></a> [recovery\_window](#input\_recovery\_window) | How many days to preserve deleted secrets before shredding. | `number` | n/a | yes |
| <a name="input_retain_n"></a> [retain\_n](#input\_retain\_n) | The number of container images to retain for this service. | `number` | n/a | yes |
| <a name="input_scaling_policy_type"></a> [scaling\_policy\_type](#input\_scaling\_policy\_type) | Which method to use when scaling the cluster. | `string` | n/a | yes |
| <a name="input_scheduled_tasks"></a> [scheduled\_tasks](#input\_scheduled\_tasks) | Data for scheduled tasks. | <pre>object({<br>    cleartokens = object({<br>      assign_public_ip    = bool,<br>      state               = string,<br>      schedule_expression = string,<br>    }),<br>    publish = object({<br>      assign_public_ip    = bool,<br>      state               = string,<br>      schedule_expression = string,<br>    }),<br>  })</pre> | n/a | yes |
| <a name="input_scheduling_strategy"></a> [scheduling\_strategy](#input\_scheduling\_strategy) | Scheduling strategy to use for the service. | `string` | n/a | yes |
| <a name="input_service_desired_count"></a> [service\_desired\_count](#input\_service\_desired\_count) | Number of ECS services running in parallel. | `number` | n/a | yes |
| <a name="input_sfn_backoff_rate"></a> [sfn\_backoff\_rate](#input\_sfn\_backoff\_rate) | Multiplier that increases the retry interval on each attempt | `number` | n/a | yes |
| <a name="input_sfn_heartbeat"></a> [sfn\_heartbeat](#input\_sfn\_heartbeat) | How long between function 'heartbeats' before timeout (cannot exceed timeout). | `number` | n/a | yes |
| <a name="input_sfn_max_attempts"></a> [sfn\_max\_attempts](#input\_sfn\_max\_attempts) | Number of times to retry a failed function. | `number` | n/a | yes |
| <a name="input_sfn_retry_interval"></a> [sfn\_retry\_interval](#input\_sfn\_retry\_interval) | How long to wait between function retries. | `number` | n/a | yes |
| <a name="input_sfn_timeout"></a> [sfn\_timeout](#input\_sfn\_timeout) | The running time threshold for a function (must exceed heartbeat). | `number` | n/a | yes |
| <a name="input_tenant_domains"></a> [tenant\_domains](#input\_tenant\_domains) | The tenanted origin(s) of the service. | `list(string)` | n/a | yes |
| <a name="input_threads"></a> [threads](#input\_threads) | Number of gunicorn threads. | `number` | n/a | yes |
| <a name="input_unmanaged_suffix"></a> [unmanaged\_suffix](#input\_unmanaged\_suffix) | Label that indicates some resource is unmanaged (rare). | `string` | n/a | yes |
| <a name="input_worker"></a> [worker](#input\_worker) | The gunicorn worker type. | `string` | n/a | yes |
| <a name="input_worker_tmp"></a> [worker\_tmp](#input\_worker\_tmp) | The gunicorn worker tmp directory. | `string` | n/a | yes |
| <a name="input_workers"></a> [workers](#input\_workers) | How many gunicorn workers to spawn. | `number` | n/a | yes |
| <a name="input_wsgi"></a> [wsgi](#input\_wsgi) | The entrypoint of the wsgi application. | `string` | n/a | yes |

## Outputs

No outputs.
<!-- END_TF_DOCS -->
