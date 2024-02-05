# Define security groups for the vpc.

resource "aws_security_group" "alb" {
  description = "Controls access to the ALB."
  name        = "${var.service}-security-group-alb-${var.environment}"
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
    Name = "${var.service}-security-group-alb-${var.environment}"
  }
}

resource "aws_security_group" "ecs" {
  description = "Allow inbound access from the ALB only."
  name        = "${var.service}-security-group-ecs-${var.environment}"
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
    Name = "${var.service}-security-group-ecs-${var.environment}"
  }
}

resource "aws_db_subnet_group" "postgres" {
  name       = "${var.service}-subnet-group-postgres-${var.environment}"
  subnet_ids = aws_subnet.private[*].id

  tags = {
    Name = "${var.service}-subnet-group-postgres-${var.environment}"
  }
}

resource "aws_security_group" "postgres" {
  description = "Allows inbound access from ECS only."
  name        = "${var.service}-security-group-postgres-${var.environment}"
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
    Name = "${var.service}-security-group-postgres-${var.environment}"
  }
}

resource "aws_security_group" "opensearch" {
  description = "Allows HTTP access from the VPC to the OpenSearch cluster"
  name        = "${var.service}-security-group-opensearch-${var.environment}"
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
    Name = "${var.service}-security-group-opensearch-${var.environment}"
  }
}
