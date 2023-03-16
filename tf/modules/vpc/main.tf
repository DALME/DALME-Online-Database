# Terraform definitions for the vpc module.

terraform {
  required_version = "~> 1.3"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.14.0"
    }
  }
}

# Fetch AZs in the current region.
data "aws_availability_zones" "available" {
  state = "available"
}

locals {
  flow_logs = "${var.service}-logs-vpc-${var.environment}-${var.aws_account}"
}

# tfsec:ignore:aws-s3-enable-bucket-encryption tfsec:ignore:aws-s3-encryption-customer-key
module "vpc_flow_logs" {
  source  = "terraform-aws-modules/s3-bucket/aws"
  version = "3.15.1"

  bucket        = local.flow_logs
  force_destroy = var.force_destroy

  acl                      = "log-delivery-write"
  control_object_ownership = true
  object_ownership         = "ObjectWriter"

  versioning = {
    enabled = true
  }

  tags = {
    Name = local.flow_logs
  }
}

resource "aws_flow_log" "vpc" {
  log_destination      = module.vpc_flow_logs.s3_bucket_arn
  log_destination_type = "s3"
  traffic_type         = "ALL"
  vpc_id               = aws_vpc.main.id

  tags = {
    Name = "${var.service}-flow-log-vpc-${var.environment}"
  }
}

resource "aws_vpc" "main" {
  cidr_block           = var.cidr
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "${var.service}-vpc-${var.environment}"
  }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${var.service}-vpc-igw-${var.environment}"
  }
}

resource "aws_eip" "nat" {
  count      = var.az_count
  domain     = "vpc"
  depends_on = [aws_internet_gateway.main]

  tags = {
    Name = "${var.service}-vpc-eip-${var.environment}-${format("%03d", count.index + 1)}"
  }
}

resource "aws_subnet" "private" {
  vpc_id            = aws_vpc.main.id
  count             = var.az_count
  cidr_block        = cidrsubnet(aws_vpc.main.cidr_block, 8, count.index)
  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = {
    Name = "${var.service}-vpc-private-subnet-${var.environment}-${format("%03d", count.index + 1)}"
  }
}

resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  count                   = var.az_count
  cidr_block              = cidrsubnet(aws_vpc.main.cidr_block, 8, var.az_count + count.index)
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = false

  tags = {
    Name = "${var.service}-vpc-public-subnet-${var.environment}-${format("%03d", count.index + 1)}"
  }
}

resource "aws_nat_gateway" "main" {
  count         = var.az_count
  subnet_id     = element(aws_subnet.public[*].id, count.index)
  allocation_id = element(aws_eip.nat[*].id, count.index)
  depends_on    = [aws_internet_gateway.main]

  tags = {
    Name = "${var.service}-vpc-ngw-${var.environment}-${format("%03d", count.index + 1)}"
  }
}

resource "aws_route_table" "private" {
  count  = var.az_count
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${var.service}-vpc-route-table-private-${var.environment}"
  }
}

resource "aws_route" "private" {
  count                  = var.az_count
  route_table_id         = element(aws_route_table.private[*].id, count.index)
  destination_cidr_block = var.destination_cidr_block
  nat_gateway_id         = element(aws_nat_gateway.main[*].id, count.index)
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${var.service}-vpc-route-table-public-${var.environment}"
  }
}

resource "aws_route" "public" {
  route_table_id         = aws_route_table.public.id
  destination_cidr_block = var.destination_cidr_block
  gateway_id             = aws_internet_gateway.main.id
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

# Security groups.
resource "aws_security_group" "alb" {
  description = "Controls access to the ALB."
  name        = "${var.service}-alb-security-group-${var.environment}"
  vpc_id      = aws_vpc.main.id

  ingress {
    description      = "Inbound HTTP."
    protocol         = var.security_groups.protocol
    from_port        = var.security_groups.proxy_port
    to_port          = var.security_groups.proxy_port
    cidr_blocks      = [var.security_groups.cidr_blocks]
    ipv6_cidr_blocks = [var.security_groups.ipv6_cidr_blocks]
  }

  ingress {
    description      = "Inbound HTTPS."
    protocol         = var.security_groups.protocol
    from_port        = var.security_groups.ssl_port
    to_port          = var.security_groups.ssl_port
    cidr_blocks      = [var.security_groups.cidr_blocks]
    ipv6_cidr_blocks = [var.security_groups.ipv6_cidr_blocks]
  }

  egress {
    description      = "Explicit ALLOW ALL outbound rule."
    protocol         = "-1"
    from_port        = 0
    to_port          = 0
    cidr_blocks      = [var.security_groups.cidr_blocks]
    ipv6_cidr_blocks = [var.security_groups.ipv6_cidr_blocks]
  }

  lifecycle {
    create_before_destroy = true
  }

  tags = {
    Name = "${var.service}-alb-security-group-${var.environment}"
  }
}

resource "aws_security_group" "ecs" {
  description = "Allow inbound access from the ALB only."
  name        = "${var.service}-ecs-security-group-${var.environment}"
  vpc_id      = aws_vpc.main.id

  ingress {
    description      = "Inbound HTTP from the ALB."
    protocol         = var.security_groups.protocol
    from_port        = var.security_groups.proxy_port
    to_port          = var.security_groups.proxy_port
    security_groups  = [aws_security_group.alb.id]
    cidr_blocks      = [var.security_groups.cidr_blocks]
    ipv6_cidr_blocks = [var.security_groups.ipv6_cidr_blocks]
  }

  egress {
    description      = "Explicit ALLOW ALL outbound rule."
    protocol         = "-1"
    from_port        = 0
    to_port          = 0
    cidr_blocks      = [var.security_groups.cidr_blocks]
    ipv6_cidr_blocks = [var.security_groups.ipv6_cidr_blocks]
  }

  lifecycle {
    create_before_destroy = true
  }

  tags = {
    Name = "${var.service}-ecs-security-group-${var.environment}"
  }
}

resource "aws_security_group" "opensearch" {
  description = "Allows HTTP access from the VPC to the OpenSearch cluster"
  name        = "${var.service}-opensearch-security-group-${var.environment}"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "Inbound HTTP from the VPC."
    protocol    = var.security_groups.protocol
    from_port   = var.security_groups.opensearch_port
    to_port     = var.security_groups.opensearch_port
    cidr_blocks = [aws_vpc.main.cidr_block]
  }

  egress {
    description      = "Explicit ALLOW ALL outbound rule."
    protocol         = "-1"
    from_port        = 0
    to_port          = 0
    cidr_blocks      = [var.security_groups.cidr_blocks]
    ipv6_cidr_blocks = [var.security_groups.ipv6_cidr_blocks]
  }

  lifecycle {
    create_before_destroy = true
  }

  tags = {
    Name = "${var.service}-opensearch-security-group-${var.environment}"
  }
}

resource "aws_security_group" "postgres" {
  description = "Allows inbound access from ECS only."
  name        = "${var.service}-postgres-security-group-${var.environment}"
  vpc_id      = aws_vpc.main.id

  ingress {
    description      = "Inbound HTTP from ECS."
    protocol         = var.security_groups.protocol
    from_port        = var.security_groups.postgres_port
    to_port          = var.security_groups.postgres_port
    security_groups  = [aws_security_group.ecs.id]
    cidr_blocks      = [var.security_groups.cidr_blocks]
    ipv6_cidr_blocks = [var.security_groups.ipv6_cidr_blocks]
  }

  egress {
    description      = "Explicit ALLOW ALL outbound rule."
    protocol         = "-1"
    from_port        = 0
    to_port          = 0
    cidr_blocks      = [var.security_groups.cidr_blocks]
    ipv6_cidr_blocks = [var.security_groups.ipv6_cidr_blocks]
  }

  lifecycle {
    create_before_destroy = true
  }

  tags = {
    Name = "${var.service}-postgres-security-group-${var.environment}"
  }
}

resource "aws_db_subnet_group" "postgres" {
  name       = "${var.service}-postgres-subnet-group-${var.environment}"
  subnet_ids = aws_subnet.private[*].id

  tags = {
    Name = "${var.service}-postgres-subnet-group-${var.environment}"
  }
}
