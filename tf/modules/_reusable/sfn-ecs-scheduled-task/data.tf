# Data sources for the sfn-ecs-scheduled-task module.

locals {
  cluster_key = "ecs-cluster"
}

data "aws_ecs_cluster" "this" {
  cluster_name = "${var.namespace}-${var.environment}-${local.cluster_key}"

  tags = {
    Namespace   = var.namespace
    Environment = var.environment
  }
}

data "aws_kms_alias" "global" {
  name = "alias/${var.namespace}/${var.environment}/global"
}

data "aws_security_group" "ecs" {
  name = "${var.namespace}-${var.environment}-${local.cluster_key}-security-group"

  tags = {
    Namespace   = var.namespace
    Environment = var.environment
  }
}

data "aws_subnets" "private" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.this.id]
  }

  tags = {
    Namespace   = var.namespace
    Environment = var.environment
    Scope       = "private"
  }
}

data "aws_vpc" "this" {
  tags = {
    Namespace   = var.namespace
    Environment = var.environment
  }
}
