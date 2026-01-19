# [VPC](https://docs.aws.amazon.com/vpc)

<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | ~> 1.14.0 |
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | 6.25.0 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | 6.25.0 |

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_vpc_eip_label"></a> [vpc\_eip\_label](#module\_vpc\_eip\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_vpc_flow_logs_label"></a> [vpc\_flow\_logs\_label](#module\_vpc\_flow\_logs\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_vpc_igw_label"></a> [vpc\_igw\_label](#module\_vpc\_igw\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_vpc_label"></a> [vpc\_label](#module\_vpc\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_vpc_ngw_label"></a> [vpc\_ngw\_label](#module\_vpc\_ngw\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_vpc_rt_private_label"></a> [vpc\_rt\_private\_label](#module\_vpc\_rt\_private\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_vpc_rt_public_label"></a> [vpc\_rt\_public\_label](#module\_vpc\_rt\_public\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_vpc_subnet_private_label"></a> [vpc\_subnet\_private\_label](#module\_vpc\_subnet\_private\_label) | cloudposse/label/null | 0.25.0 |
| <a name="module_vpc_subnet_public_label"></a> [vpc\_subnet\_public\_label](#module\_vpc\_subnet\_public\_label) | cloudposse/label/null | 0.25.0 |

## Resources

| Name | Type |
|------|------|
| [aws_eip.nat](https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/eip) | resource |
| [aws_flow_log.vpc](https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/flow_log) | resource |
| [aws_internet_gateway.this](https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/internet_gateway) | resource |
| [aws_nat_gateway.this](https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/nat_gateway) | resource |
| [aws_route.private](https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/route) | resource |
| [aws_route.public](https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/route) | resource |
| [aws_route_table.private](https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/route_table) | resource |
| [aws_route_table.public](https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/route_table) | resource |
| [aws_route_table_association.private](https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/route_table_association) | resource |
| [aws_route_table_association.public](https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/route_table_association) | resource |
| [aws_subnet.private](https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/subnet) | resource |
| [aws_subnet.public](https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/subnet) | resource |
| [aws_vpc.this](https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/vpc) | resource |
| [aws_availability_zones.available](https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/data-sources/availability_zones) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_az_count"></a> [az\_count](#input\_az\_count) | Number of availability zones in a given region. | `number` | n/a | yes |
| <a name="input_cidr"></a> [cidr](#input\_cidr) | The IPv4 CIDR block for the VPC. | `string` | n/a | yes |
| <a name="input_destination_cidr_block"></a> [destination\_cidr\_block](#input\_destination\_cidr\_block) | The CIDR block associated with the local subnet. | `string` | n/a | yes |
| <a name="input_environment"></a> [environment](#input\_environment) | Identify the deployment environment. | `string` | n/a | yes |
| <a name="input_log_destination"></a> [log\_destination](#input\_log\_destination) | Optional ARN of a resource to receive VPC flow logs. | `string` | `null` | no |
| <a name="input_log_destination_type"></a> [log\_destination\_type](#input\_log\_destination\_type) | The type of the logging destination. | `string` | `null` | no |
| <a name="input_namespace"></a> [namespace](#input\_namespace) | The project namespace. | `string` | n/a | yes |
| <a name="input_service"></a> [service](#input\_service) | An optional service namespace. | `string` | `null` | no |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_subnets"></a> [subnets](#output\_subnets) | Bundle VPC subnet identifiers. |
| <a name="output_vpc_id"></a> [vpc\_id](#output\_vpc\_id) | Identifier for the VPC. |
<!-- END_TF_DOCS -->