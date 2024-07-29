Cdn

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
| <a name="module_access_logs"></a> [access\_logs](#module\_access\_logs) | ../..//_reusable/bucket/ | n/a |
| <a name="module_assets"></a> [assets](#module\_assets) | ../..//_reusable/bucket/ | n/a |
| <a name="module_cdn_access_logs_label"></a> [cdn\_access\_logs\_label](#module\_cdn\_access\_logs\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_cdn_label"></a> [cdn\_label](#module\_cdn\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_cloudfront"></a> [cloudfront](#module\_cloudfront) | ../..//_reusable/cloudfront/ | n/a |
| <a name="module_staticfiles"></a> [staticfiles](#module\_staticfiles) | ../..//_reusable/bucket/ | n/a |

## Resources

| Name | Type |
|------|------|
| [aws_cloudfront_function.viewer_request](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/resources/cloudfront_function) | resource |
| [aws_cloudfront_origin_access_control.s3](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/resources/cloudfront_origin_access_control) | resource |
| [aws_route53_record.www-a](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/resources/route53_record) | resource |
| [aws_route53_record.www-aaaa](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/resources/route53_record) | resource |
| [aws_s3_bucket_policy.oac_assets](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/resources/s3_bucket_policy) | resource |
| [aws_s3_bucket_policy.oac_staticfiles](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/resources/s3_bucket_policy) | resource |
| [aws_iam_policy_document.oac_assets](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.oac_staticfiles](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/data-sources/iam_policy_document) | data source |
| [aws_lb.this](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/data-sources/lb) | data source |
| [aws_route53_zone.tenant_zones](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/data-sources/route53_zone) | data source |
| [aws_wafv2_web_acl.this](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/data-sources/wafv2_web_acl) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_default_root_object"></a> [default\_root\_object](#input\_default\_root\_object) | The object to return (for example, index.html) the root URL is requested. | `string` | `null` | no |
| <a name="input_dns_ttl"></a> [dns\_ttl](#input\_dns\_ttl) | Time to live for the certificate DNS record. | `number` | n/a | yes |
| <a name="input_domain"></a> [domain](#input\_domain) | The origin of the service. | `string` | n/a | yes |
| <a name="input_force_destroy"></a> [force\_destroy](#input\_force\_destroy) | Whether deletion protection is active on buckets. | `bool` | n/a | yes |
| <a name="input_price_class"></a> [price\_class](#input\_price\_class) | Selects the price class for the distribution. | `string` | n/a | yes |

## Outputs

No outputs.
<!-- END_TF_DOCS -->