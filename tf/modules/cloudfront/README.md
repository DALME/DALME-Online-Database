<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | ~> 1.3 |
| <a name="requirement_archive"></a> [archive](#requirement\_archive) | 2.4.0 |
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | 5.14.0 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | 5.14.0 |
| <a name="provider_aws.acm"></a> [aws.acm](#provider\_aws.acm) | 5.14.0 |

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_access_logs"></a> [access\_logs](#module\_access\_logs) | terraform-aws-modules/s3-bucket/aws | 3.15.1 |
| <a name="module_assets"></a> [assets](#module\_assets) | terraform-aws-modules/s3-bucket/aws | 3.15.1 |
| <a name="module_staticfiles"></a> [staticfiles](#module\_staticfiles) | terraform-aws-modules/s3-bucket/aws | 3.15.1 |

## Resources

| Name | Type |
|------|------|
| [aws_acm_certificate.cloudfront](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/acm_certificate) | resource |
| [aws_acm_certificate_validation.cloudfront](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/acm_certificate_validation) | resource |
| [aws_cloudfront_distribution.main](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/cloudfront_distribution) | resource |
| [aws_cloudfront_function.viewer_request](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/cloudfront_function) | resource |
| [aws_cloudfront_origin_access_control.s3](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/cloudfront_origin_access_control) | resource |
| [aws_route53_record.cloudfront](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/route53_record) | resource |
| [aws_route53_record.www-a](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/route53_record) | resource |
| [aws_route53_record.www-aaaa](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/route53_record) | resource |
| [aws_s3_bucket_policy.oac_assets](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/s3_bucket_policy) | resource |
| [aws_s3_bucket_policy.oac_staticfiles](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/s3_bucket_policy) | resource |
| [aws_s3_bucket_policy.public_staticfiles](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/s3_bucket_policy) | resource |
| [aws_iam_policy_document.oac_assets](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.oac_staticfiles](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.public_staticfiles](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/data-sources/iam_policy_document) | data source |
| [aws_route53_zone.tenant_zones](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/data-sources/route53_zone) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_alb_dns"></a> [alb\_dns](#input\_alb\_dns) | Load balancer DNS endpoint. | `string` | n/a | yes |
| <a name="input_allowed_methods"></a> [allowed\_methods](#input\_allowed\_methods) | Permissable HTTP verbs for this distribution. | `list(string)` | n/a | yes |
| <a name="input_aws_account"></a> [aws\_account](#input\_aws\_account) | The AWS account where resources are created. | `number` | n/a | yes |
| <a name="input_dns_ttl"></a> [dns\_ttl](#input\_dns\_ttl) | Time to live for the certificate DNS record. | `number` | n/a | yes |
| <a name="input_environment"></a> [environment](#input\_environment) | Identify the deployment environment. | `string` | n/a | yes |
| <a name="input_force_destroy"></a> [force\_destroy](#input\_force\_destroy) | Whether deletion protection is active on the module buckets. | `bool` | n/a | yes |
| <a name="input_service"></a> [service](#input\_service) | The service of the project/stack. | `string` | n/a | yes |
| <a name="input_tenant_domains"></a> [tenant\_domains](#input\_tenant\_domains) | The origin(s) of the service. | `list(string)` | n/a | yes |
| <a name="input_web_acl_id"></a> [web\_acl\_id](#input\_web\_acl\_id) | Identifier for the WAF. | `string` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_arn"></a> [arn](#output\_arn) | ARN for the distribution. |
| <a name="output_assets_arn"></a> [assets\_arn](#output\_assets\_arn) | The ARN of the s3 bucket containing frontend assets. |
| <a name="output_domain"></a> [domain](#output\_domain) | Where the destribution is served. |
| <a name="output_staticfiles_arn"></a> [staticfiles\_arn](#output\_staticfiles\_arn) | The ARN of the s3 bucket containing static and media files. |
| <a name="output_staticfiles_bucket"></a> [staticfiles\_bucket](#output\_staticfiles\_bucket) | The name of the s3 bucket containing static and media files. |
| <a name="output_staticfiles_domain"></a> [staticfiles\_domain](#output\_staticfiles\_domain) | The s3 bucket's regionally qualified endpoint. |
<!-- END_TF_DOCS -->