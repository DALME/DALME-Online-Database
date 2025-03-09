# [Elastic Load Balancer](https://docs.aws.amazon.com/elasticloadbalancing)

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
| <a name="module_alb_certificate_label"></a> [alb\_certificate\_label](#module\_alb\_certificate\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_alb_http_label"></a> [alb\_http\_label](#module\_alb\_http\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_alb_https_label"></a> [alb\_https\_label](#module\_alb\_https\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_alb_label"></a> [alb\_label](#module\_alb\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_alb_sg_label"></a> [alb\_sg\_label](#module\_alb\_sg\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_alb_tg_label"></a> [alb\_tg\_label](#module\_alb\_tg\_label) | cloudposse/label/null | 0.25.0 |

## Resources

| Name | Type |
|------|------|
| [aws_acm_certificate.alb](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/resources/acm_certificate) | resource |
| [aws_acm_certificate_validation.alb](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/resources/acm_certificate_validation) | resource |
| [aws_lb.this](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/resources/lb) | resource |
| [aws_lb_listener.http](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/resources/lb_listener) | resource |
| [aws_lb_listener.https](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/resources/lb_listener) | resource |
| [aws_lb_target_group.this](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/resources/lb_target_group) | resource |
| [aws_route53_record.alb](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/resources/route53_record) | resource |
| [aws_security_group.alb](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/resources/security_group) | resource |
| [aws_route53_zone.tenant_zones](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/data-sources/route53_zone) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_additional_domains"></a> [additional\_domains](#input\_additional\_domains) | Other domains to be served by this ALB. | `list(string)` | n/a | yes |
| <a name="input_alb_port"></a> [alb\_port](#input\_alb\_port) | Load balancer listening port. | `number` | n/a | yes |
| <a name="input_dns_ttl"></a> [dns\_ttl](#input\_dns\_ttl) | Time to live for the certificate's DNS record. | `number` | n/a | yes |
| <a name="input_domain"></a> [domain](#input\_domain) | The origin of the service. | `string` | n/a | yes |
| <a name="input_environment"></a> [environment](#input\_environment) | Identify the deployment environment. | `string` | n/a | yes |
| <a name="input_force_destroy"></a> [force\_destroy](#input\_force\_destroy) | Whether deletion protection is active on buckets. | `bool` | n/a | yes |
| <a name="input_health_check"></a> [health\_check](#input\_health\_check) | Parameters configuring the ALB's healthcheck. | <pre>object({<br>    interval            = number, # Frequency (secs) of the health checks.<br>    matcher             = number, # HTTP status code indicating a passing health check.<br>    path                = string, # URL route of the healthcheck.<br>    threshold           = number, # Count before considering an unhealthy target healthy.<br>    timeout             = number, # Time (secs) without a response indicting a failed health check.<br>    unhealthy_threshold = number, # Consecutive failed health checks before considering a target unhealthy.<br>  })</pre> | n/a | yes |
| <a name="input_internal"></a> [internal](#input\_internal) | Should this ALB have a public IP or not. | `bool` | n/a | yes |
| <a name="input_log_destination"></a> [log\_destination](#input\_log\_destination) | Bucket to hold the ALB access logs. | `string` | n/a | yes |
| <a name="input_log_prefix"></a> [log\_prefix](#input\_log\_prefix) | String to prepend to the S3 bucket destination. | `string` | n/a | yes |
| <a name="input_logging_enabled"></a> [logging\_enabled](#input\_logging\_enabled) | Should this ALB write to logs. | `bool` | n/a | yes |
| <a name="input_namespace"></a> [namespace](#input\_namespace) | The project namespace. | `string` | n/a | yes |
| <a name="input_service"></a> [service](#input\_service) | An optional service namespace. | `string` | `null` | no |
| <a name="input_ssl_port"></a> [ssl\_port](#input\_ssl\_port) | Secure HTTPS listening port. | `number` | n/a | yes |
| <a name="input_subnets"></a> [subnets](#input\_subnets) | Public subnets of the VPC. | `list(string)` | n/a | yes |
| <a name="input_vpc_id"></a> [vpc\_id](#input\_vpc\_id) | Identifier for the VPC. | `string` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_security_group_id"></a> [security\_group\_id](#output\_security\_group\_id) | Identify the security group controlling access to the ALB. |
| <a name="output_security_group_label_context"></a> [security\_group\_label\_context](#output\_security\_group\_label\_context) | Label data for the ALB security group. |
<!-- END_TF_DOCS -->