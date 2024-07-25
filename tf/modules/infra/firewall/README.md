Firewall

<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | ~> 1.6 |
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | 5.59.0 |

## Providers

No providers.

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_waf"></a> [waf](#module\_waf) | ../..//_reusable/waf/ | n/a |
| <a name="module_waf_logs"></a> [waf\_logs](#module\_waf\_logs) | ../..//_reusable/bucket/ | n/a |
| <a name="module_waf_logs_label"></a> [waf\_logs\_label](#module\_waf\_logs\_label) | cloudposse/label/null | 0.25.0 |

## Resources

No resources.

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_countries"></a> [countries](#input\_countries) | A list of country codes for scoping geo rules. | `list(string)` | n/a | yes |
| <a name="input_force_destroy"></a> [force\_destroy](#input\_force\_destroy) | Whether deletion protection is active on the logging buckets. | `bool` | n/a | yes |
| <a name="input_ipv4_ip_set_addresses"></a> [ipv4\_ip\_set\_addresses](#input\_ipv4\_ip\_set\_addresses) | IPV4 format addresses for the firewall. | `list(string)` | n/a | yes |
| <a name="input_ipv6_ip_set_addresses"></a> [ipv6\_ip\_set\_addresses](#input\_ipv6\_ip\_set\_addresses) | IPV6 format addresses for the firewall. | `list(string)` | n/a | yes |
| <a name="input_lifecycle_rule"></a> [lifecycle\_rule](#input\_lifecycle\_rule) | Configuration for the logging bucket lifecycle. | <pre>object({<br>    expiration_days            = number,<br>    noncurrent_expiration_days = number,<br>    noncurrent_transition_days = number,<br>    storage_class              = string,<br>  })</pre> | <pre>{<br>  "expiration_days": 90,<br>  "noncurrent_expiration_days": 90,<br>  "noncurrent_transition_days": 30,<br>  "storage_class": "STANDARD_IA"<br>}</pre> | no |
| <a name="input_rules"></a> [rules](#input\_rules) | Data for settings parameters in the rule declarations. | <pre>object({<br>    domestic_dos_limit = number,<br>    global_dos_limit   = number,<br>  })</pre> | n/a | yes |

## Outputs

No outputs.
<!-- END_TF_DOCS -->