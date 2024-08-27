# [EC2 Instance](https://aws.amazon.com/ec2)

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
| <a name="module_ec2_label"></a> [ec2\_label](#module\_ec2\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_ec2_label_sg"></a> [ec2\_label\_sg](#module\_ec2\_label\_sg) | cloudposse/label/null | 0.25.0 |

## Resources

| Name | Type |
|------|------|
| [aws_launch_template.this](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/resources/launch_template) | resource |
| [aws_security_group.this](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/resources/security_group) | resource |
| [aws_ami.this](https://registry.terraform.io/providers/hashicorp/aws/5.59.0/docs/data-sources/ami) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_ami_filters"></a> [ami\_filters](#input\_ami\_filters) | One or more name/value pairs to filter down the ami data source. | `list(object({ name = string, values = list(string) }))` | `null` | no |
| <a name="input_ami_most_recent"></a> [ami\_most\_recent](#input\_ami\_most\_recent) | If more than one ami result is returned, use the most recent. | `bool` | `true` | no |
| <a name="input_ami_name_regex"></a> [ami\_name\_regex](#input\_ami\_name\_regex) | Regex for filtering down the ami data source. | `string` | n/a | yes |
| <a name="input_ami_owners"></a> [ami\_owners](#input\_ami\_owners) | List of AMI owners for filtering down the ami data source | `list(string)` | <pre>[<br>  "amazon"<br>]</pre> | no |
| <a name="input_environment"></a> [environment](#input\_environment) | Identify the deployment environment. | `string` | n/a | yes |
| <a name="input_iam_instance_profile_name"></a> [iam\_instance\_profile\_name](#input\_iam\_instance\_profile\_name) | The IAM Instance Profile to attach to the instance. | `string` | n/a | yes |
| <a name="input_instance_type"></a> [instance\_type](#input\_instance\_type) | The type of the ec2 instance. | `string` | n/a | yes |
| <a name="input_metadata_options"></a> [metadata\_options](#input\_metadata\_options) | Metadata configuration for the instance. | <pre>object({<br>    http_endpoint               = string,<br>    http_put_response_hop_limit = number,<br>    http_protocol_ipv6          = optional(string),<br>    instance_metadata_tags      = string<br>  })</pre> | n/a | yes |
| <a name="input_monitoring"></a> [monitoring](#input\_monitoring) | Should the EC2 instance have detailed monitoring enabled. | `bool` | `true` | no |
| <a name="input_name"></a> [name](#input\_name) | The name of the launch template. | `string` | n/a | yes |
| <a name="input_namespace"></a> [namespace](#input\_namespace) | The project namespace. | `string` | n/a | yes |
| <a name="input_network_interfaces"></a> [network\_interfaces](#input\_network\_interfaces) | Attach one or more network interfaces to the instance. | <pre>list(object({<br>    associate_public_ip_address = bool,<br>    delete_on_termination       = bool,<br>    security_groups             = optional(list(string)),<br>    subnet_id                   = optional(string),<br>  }))</pre> | n/a | yes |
| <a name="input_update_default_version"></a> [update\_default\_version](#input\_update\_default\_version) | Bump the default version of the instance on each update. | `bool` | `true` | no |
| <a name="input_vpc_id"></a> [vpc\_id](#input\_vpc\_id) | Identifier for the VPC. | `string` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_launch_template_id"></a> [launch\_template\_id](#output\_launch\_template\_id) | Identifier for the ec2 launch template. |
| <a name="output_launch_template_latest_version"></a> [launch\_template\_latest\_version](#output\_launch\_template\_latest\_version) | Latest version of the ec2 launch template. |
| <a name="output_security_group_id"></a> [security\_group\_id](#output\_security\_group\_id) | Identifier for the ec2 instance's security group (if created). |
<!-- END_TF_DOCS -->