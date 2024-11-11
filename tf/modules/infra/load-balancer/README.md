# Load-balancer

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
| <a name="module_alb"></a> [alb](#module\_alb) | ../..//_reusable/alb/ | n/a |
| <a name="module_alb_access_logs"></a> [alb\_access\_logs](#module\_alb\_access\_logs) | ../..//_reusable/bucket/ | n/a |

## Resources

| Name | Type |
|------|------|
| [aws_s3_bucket_policy.alb_logs](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/resources/s3_bucket_policy) | resource |
| [aws_security_group_rule.alb_egress](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/resources/security_group_rule) | resource |
| [aws_security_group_rule.alb_ingress_http](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/resources/security_group_rule) | resource |
| [aws_security_group_rule.alb_ingress_https](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/resources/security_group_rule) | resource |
| [aws_elb_service_account.this](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/data-sources/elb_service_account) | data source |
| [aws_iam_policy_document.alb_logs](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/data-sources/iam_policy_document) | data source |
| [aws_subnets.public](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/data-sources/subnets) | data source |
| [aws_vpc.this](https://registry.terraform.io/providers/hashicorp/aws/5.70.0/docs/data-sources/vpc) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_additional_domains"></a> [additional\_domains](#input\_additional\_domains) | Other domains to be served by this load balancer. | `list(string)` | n/a | yes |
| <a name="input_alb_port"></a> [alb\_port](#input\_alb\_port) | Load balancer listening port. | `number` | n/a | yes |
| <a name="input_cidr_blocks"></a> [cidr\_blocks](#input\_cidr\_blocks) | IPv4 range for the ALB security groups. | `string` | n/a | yes |
| <a name="input_dns_ttl"></a> [dns\_ttl](#input\_dns\_ttl) | Time to live for the certificate DNS record. | `number` | n/a | yes |
| <a name="input_domain"></a> [domain](#input\_domain) | The origin of the service. | `string` | n/a | yes |
| <a name="input_force_destroy"></a> [force\_destroy](#input\_force\_destroy) | Whether deletion protection is active on buckets. | `bool` | n/a | yes |
| <a name="input_health_check"></a> [health\_check](#input\_health\_check) | Parameters configuring the ALB's healthcheck. | <pre>object({<br>    interval            = number, # Frequency (secs) of the health checks.<br>    matcher             = number, # HTTP status code indicating a passing health check.<br>    path                = string, # URL route of the healthcheck.<br>    threshold           = number, # Count before considering an unhealthy target healthy.<br>    timeout             = number, # Time (secs) without a response indicting a failed health check.<br>    unhealthy_threshold = number, # Consecutive failed health checks before considering a target unhealthy.<br>  })</pre> | n/a | yes |
| <a name="input_internal"></a> [internal](#input\_internal) | Should this ALB have a public IP or not. | `bool` | n/a | yes |
| <a name="input_ipv6_cidr_blocks"></a> [ipv6\_cidr\_blocks](#input\_ipv6\_cidr\_blocks) | IPv6 range for the ALB security groups. | `string` | n/a | yes |
| <a name="input_protocol"></a> [protocol](#input\_protocol) | Transport protocol for the security group. | `string` | n/a | yes |
| <a name="input_proxy_port"></a> [proxy\_port](#input\_proxy\_port) | Reverse proxy listening port. | `number` | n/a | yes |
| <a name="input_ssl_port"></a> [ssl\_port](#input\_ssl\_port) | Secure HTTPS listening port. | `number` | n/a | yes |

## Outputs

No outputs.
<!-- END_TF_DOCS -->