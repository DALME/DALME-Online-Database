# [Cloudfront](https://docs.aws.amazon.com/cloudfront/)

<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | ~> 1.6 |
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | 5.59.0 |
| <a name="requirement_tls"></a> [tls](#requirement\_tls) | 4.0.5 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | 5.59.0 |

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_cloudfront_certificate_label"></a> [cloudfront\_certificate\_label](#module\_cloudfront\_certificate\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_cloudfront_label"></a> [cloudfront\_label](#module\_cloudfront\_label) | cloudposse/label/null | 0.25.0 |

## Resources

| Name | Type |
|------|------|
| [aws_acm_certificate.cloudfront](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/resources/acm_certificate) | resource |
| [aws_acm_certificate_validation.cloudfront](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/resources/acm_certificate_validation) | resource |
| [aws_cloudfront_distribution.this](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/resources/cloudfront_distribution) | resource |
| [aws_route53_record.cloudfront](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/resources/route53_record) | resource |
| [aws_route53_zone.tenant_zones](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/data-sources/route53_zone) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_additional_domains"></a> [additional\_domains](#input\_additional\_domains) | Other domains to be served by this distribution. | `list(string)` | n/a | yes |
| <a name="input_aliases"></a> [aliases](#input\_aliases) | Extra CNAMEs (alternate domain names), if any, for this distribution. | `list(string)` | `null` | no |
| <a name="input_default_cache_behavior"></a> [default\_cache\_behavior](#input\_default\_cache\_behavior) | The default cache definition for the distribution. | `any` | n/a | yes |
| <a name="input_default_root_object"></a> [default\_root\_object](#input\_default\_root\_object) | The object to return (for example, index.html) the root URL is requested. | `string` | `null` | no |
| <a name="input_dns_ttl"></a> [dns\_ttl](#input\_dns\_ttl) | Time to live for the certificate DNS record. | `number` | n/a | yes |
| <a name="input_domain"></a> [domain](#input\_domain) | The origin of the service. | `string` | n/a | yes |
| <a name="input_environment"></a> [environment](#input\_environment) | Identify the deployment environment. | `string` | n/a | yes |
| <a name="input_geo_restriction"></a> [geo\_restriction](#input\_geo\_restriction) | The geo restriction configuration for the distribution. | `any` | `{}` | no |
| <a name="input_log_destination"></a> [log\_destination](#input\_log\_destination) | Bucket to receive the distribution access logs. | `string` | n/a | yes |
| <a name="input_namespace"></a> [namespace](#input\_namespace) | The project namespace. | `string` | n/a | yes |
| <a name="input_ordered_cache_behavior"></a> [ordered\_cache\_behavior](#input\_ordered\_cache\_behavior) | An ordered list of cache behaviors for the distribution. The topmost cache behavior will have precedence 0 and so on. | `any` | `[]` | no |
| <a name="input_origin"></a> [origin](#input\_origin) | One or more origins for the distribution. | `any` | n/a | yes |
| <a name="input_price_class"></a> [price\_class](#input\_price\_class) | Selects the price class for the distribution. | `string` | n/a | yes |
| <a name="input_service"></a> [service](#input\_service) | An optional service namespace. | `string` | `null` | no |
| <a name="input_web_acl_id"></a> [web\_acl\_id](#input\_web\_acl\_id) | Identifier for the WAF. | `string` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_arn"></a> [arn](#output\_arn) | ARN for the distribution. |
<!-- END_TF_DOCS -->