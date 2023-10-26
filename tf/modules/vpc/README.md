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

| Name | Source | Version |
|------|--------|---------|
| <a name="module_vpc_flow_logs"></a> [vpc\_flow\_logs](#module\_vpc\_flow\_logs) | terraform-aws-modules/s3-bucket/aws | 3.15.1 |

## Resources

| Name | Type |
|------|------|
| [aws_acm_certificate.vpn](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/acm_certificate) | resource |
| [aws_acm_certificate_validation.vpn](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/acm_certificate_validation) | resource |
| [aws_db_subnet_group.postgres](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/db_subnet_group) | resource |
| [aws_eip.nat](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/eip) | resource |
| [aws_flow_log.vpc](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/flow_log) | resource |
| [aws_internet_gateway.main](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/internet_gateway) | resource |
| [aws_nat_gateway.main](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/nat_gateway) | resource |
| [aws_route.private](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/route) | resource |
| [aws_route.public](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/route) | resource |
| [aws_route53_record.vpn](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/route53_record) | resource |
| [aws_route_table.private](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/route_table) | resource |
| [aws_route_table.public](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/route_table) | resource |
| [aws_route_table_association.private](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/route_table_association) | resource |
| [aws_route_table_association.public](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/route_table_association) | resource |
| [aws_security_group.alb](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/security_group) | resource |
| [aws_security_group.ecs](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/security_group) | resource |
| [aws_security_group.opensearch](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/security_group) | resource |
| [aws_security_group.postgres](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/security_group) | resource |
| [aws_subnet.private](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/subnet) | resource |
| [aws_subnet.public](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/subnet) | resource |
| [aws_vpc.main](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/resources/vpc) | resource |
| [aws_availability_zones.available](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/data-sources/availability_zones) | data source |
| [aws_route53_zone.main](https://registry.terraform.io/providers/hashicorp/aws/5.14.0/docs/data-sources/route53_zone) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_aws_account"></a> [aws\_account](#input\_aws\_account) | The AWS account where resources are created. | `number` | n/a | yes |
| <a name="input_az_count"></a> [az\_count](#input\_az\_count) | Number of availability zones in a given region. | `number` | n/a | yes |
| <a name="input_cidr"></a> [cidr](#input\_cidr) | The IPv4 CIDR block for the VPC. | `string` | n/a | yes |
| <a name="input_destination_cidr_block"></a> [destination\_cidr\_block](#input\_destination\_cidr\_block) | The CIDR block associated with the local subnet. | `string` | n/a | yes |
| <a name="input_environment"></a> [environment](#input\_environment) | Identify the deployment environment. | `string` | n/a | yes |
| <a name="input_force_destroy"></a> [force\_destroy](#input\_force\_destroy) | Whether deletion protection is active on the module buckets. | `bool` | n/a | yes |
| <a name="input_security_groups"></a> [security\_groups](#input\_security\_groups) | Common data for instantiating security groups. | <pre>object({<br>    cidr_blocks      = string,<br>    ipv6_cidr_blocks = string,<br>    protocol         = string,<br>    opensearch_port  = number,<br>    postgres_port    = number,<br>    proxy_port       = number,<br>    ssl_port         = number,<br>  })</pre> | n/a | yes |
| <a name="input_service"></a> [service](#input\_service) | The service of the project/stack. | `string` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_security_groups"></a> [security\_groups](#output\_security\_groups) | Bundles security group identifiers. |
| <a name="output_subnets"></a> [subnets](#output\_subnets) | Bundles subnet identifiers. |
| <a name="output_vpc_id"></a> [vpc\_id](#output\_vpc\_id) | Identifier for the VPC. |
<!-- END_TF_DOCS -->