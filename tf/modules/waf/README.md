<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | ~> 1.3 |
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | 5.14.0 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_aws.acm"></a> [aws.acm](#provider\_aws.acm) | 5.14.0 |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [aws_s3_bucket.waf](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/s3_bucket) | resource |
| [aws_s3_bucket_acl.waf](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/s3_bucket_acl) | resource |
| [aws_s3_bucket_ownership_controls.waf](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/s3_bucket_ownership_controls) | resource |
| [aws_s3_bucket_public_access_block.waf](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/s3_bucket_public_access_block) | resource |
| [aws_s3_bucket_versioning.waf](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/s3_bucket_versioning) | resource |
| [aws_wafv2_ip_set.ipv4](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/wafv2_ip_set) | resource |
| [aws_wafv2_ip_set.ipv6](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/wafv2_ip_set) | resource |
| [aws_wafv2_web_acl.main](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/wafv2_web_acl) | resource |
| [aws_wafv2_web_acl_logging_configuration.waf](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/wafv2_web_acl_logging_configuration) | resource |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_aws_account"></a> [aws\_account](#input\_aws\_account) | The AWS account where resources are created. | `number` | n/a | yes |
| <a name="input_country"></a> [country](#input\_country) | A country code for scoping geo rules. | `string` | n/a | yes |
| <a name="input_environment"></a> [environment](#input\_environment) | Identify the deployment environment. | `string` | n/a | yes |
| <a name="input_force_destroy"></a> [force\_destroy](#input\_force\_destroy) | Whether deletion protection is active on the module buckets. | `bool` | n/a | yes |
| <a name="input_name"></a> [name](#input\_name) | The name of the WAF instance. | `string` | n/a | yes |
| <a name="input_service"></a> [service](#input\_service) | The service of the project/stack. | `string` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_waf_arn"></a> [waf\_arn](#output\_waf\_arn) | ARN of the WAF itself. |
| <a name="output_waf_ipsets_cloudfront_ipv4_arn"></a> [waf\_ipsets\_cloudfront\_ipv4\_arn](#output\_waf\_ipsets\_cloudfront\_ipv4\_arn) | IPv4 blacklist ARN |
| <a name="output_waf_ipsets_cloudfront_ipv6_arn"></a> [waf\_ipsets\_cloudfront\_ipv6\_arn](#output\_waf\_ipsets\_cloudfront\_ipv6\_arn) | IPv6 blacklist ARN |
<!-- END_TF_DOCS -->