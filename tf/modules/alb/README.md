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
| [aws_acm_certificate.alb](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/acm_certificate) | resource |
| [aws_acm_certificate_validation.alb](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/acm_certificate_validation) | resource |
| [aws_lb.main](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/lb) | resource |
| [aws_lb_listener.http](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/lb_listener) | resource |
| [aws_lb_listener.https](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/lb_listener) | resource |
| [aws_lb_target_group.main](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/lb_target_group) | resource |
| [aws_route53_record.alb](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/route53_record) | resource |
| [aws_route53_zone.tenant_zones](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/data-sources/route53_zone) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_alb_port"></a> [alb\_port](#input\_alb\_port) | Load balancer listening port. | `number` | n/a | yes |
| <a name="input_dns_ttl"></a> [dns\_ttl](#input\_dns\_ttl) | Time to live for the certificate DNS record. | `number` | n/a | yes |
| <a name="input_environment"></a> [environment](#input\_environment) | Identify the deployment environment. | `string` | n/a | yes |
| <a name="input_health_check_interval"></a> [health\_check\_interval](#input\_health\_check\_interval) | Frequency (secs) of the health checks | `number` | n/a | yes |
| <a name="input_health_check_matcher"></a> [health\_check\_matcher](#input\_health\_check\_matcher) | HTTP status code indicating a passing health check. | `number` | n/a | yes |
| <a name="input_health_check_path"></a> [health\_check\_path](#input\_health\_check\_path) | Application smoke test endpoint. | `string` | n/a | yes |
| <a name="input_health_check_threshold"></a> [health\_check\_threshold](#input\_health\_check\_threshold) | Health check count before considering an unhealthy target healthy. | `number` | n/a | yes |
| <a name="input_health_check_timeout"></a> [health\_check\_timeout](#input\_health\_check\_timeout) | Time (secs) without a response indicting a failed health check. | `number` | n/a | yes |
| <a name="input_health_check_unhealthy_threshold"></a> [health\_check\_unhealthy\_threshold](#input\_health\_check\_unhealthy\_threshold) | Consecutive failed health checks before considering a target unhealthy. | `number` | n/a | yes |
| <a name="input_security_groups"></a> [security\_groups](#input\_security\_groups) | The security group for the alb. | `list(string)` | n/a | yes |
| <a name="input_service"></a> [service](#input\_service) | The service of the project/stack. | `string` | n/a | yes |
| <a name="input_ssl_port"></a> [ssl\_port](#input\_ssl\_port) | Secure HTTPS listening port. | `number` | n/a | yes |
| <a name="input_subnets"></a> [subnets](#input\_subnets) | The (public) VPC subnets in which to register the ALB. | `list(string)` | n/a | yes |
| <a name="input_tenant_domains"></a> [tenant\_domains](#input\_tenant\_domains) | The origin(s) of the service. | `list(string)` | n/a | yes |
| <a name="input_vpc_id"></a> [vpc\_id](#input\_vpc\_id) | Identifier for the VPC. | `string` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_dns"></a> [dns](#output\_dns) | Load balancer DNS endpoint. |
| <a name="output_target_group_arn"></a> [target\_group\_arn](#output\_target\_group\_arn) | The target group for the ALB. |
<!-- END_TF_DOCS -->