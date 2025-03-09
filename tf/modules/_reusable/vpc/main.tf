# Entrypoint for the vpc module.

resource "aws_vpc" "this" {
  cidr_block           = var.cidr
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = module.vpc_label.tags
}

resource "aws_internet_gateway" "this" {
  vpc_id = aws_vpc.this.id

  tags = module.vpc_igw_label.tags
}

resource "aws_eip" "nat" {
  count      = var.az_count
  domain     = "vpc"
  depends_on = [aws_internet_gateway.this]

  tags = module.vpc_eip_label.tags
}

resource "aws_subnet" "private" {
  count             = var.az_count
  vpc_id            = aws_vpc.this.id
  cidr_block        = cidrsubnet(aws_vpc.this.cidr_block, 8, count.index)
  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = module.vpc_subnet_private_label.tags
}

resource "aws_subnet" "public" {
  count             = var.az_count
  vpc_id            = aws_vpc.this.id
  cidr_block        = cidrsubnet(aws_vpc.this.cidr_block, 8, var.az_count + count.index)
  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = module.vpc_subnet_public_label.tags
}

resource "aws_nat_gateway" "this" {
  count         = var.az_count
  subnet_id     = element(aws_subnet.public[*].id, count.index)
  allocation_id = element(aws_eip.nat[*].id, count.index)
  depends_on    = [aws_internet_gateway.this]

  tags = module.vpc_ngw_label.tags
}

resource "aws_route_table" "private" {
  count  = var.az_count
  vpc_id = aws_vpc.this.id

  tags = module.vpc_rt_private_label.tags
}

resource "aws_route" "private" {
  count                  = var.az_count
  route_table_id         = element(aws_route_table.private[*].id, count.index)
  destination_cidr_block = var.destination_cidr_block
  nat_gateway_id         = element(aws_nat_gateway.this[*].id, count.index)
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.this.id

  tags = module.vpc_rt_public_label.tags
}

resource "aws_route" "public" {
  route_table_id         = aws_route_table.public.id
  destination_cidr_block = var.destination_cidr_block
  gateway_id             = aws_internet_gateway.this.id
}

resource "aws_route_table_association" "private" {
  count          = var.az_count
  subnet_id      = element(aws_subnet.private[*].id, count.index)
  route_table_id = element(aws_route_table.private[*].id, count.index)
}

resource "aws_route_table_association" "public" {
  count          = var.az_count
  subnet_id      = element(aws_subnet.public[*].id, count.index)
  route_table_id = aws_route_table.public.id
}

# Note: If you ever want to direct this somewhere other than a bucket,
# cloudwatch or kinesis for example, you'll need to add further configuration.
# https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/flow_log
resource "aws_flow_log" "vpc" {
  log_destination      = var.log_destination
  log_destination_type = var.log_destination_type
  traffic_type         = "ALL"
  vpc_id               = aws_vpc.this.id

  tags = module.vpc_flow_logs_label.tags
}
