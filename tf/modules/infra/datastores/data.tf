# Data sources for the datastores module.
#
# Any dependencies between this node and ancestors on the environment DAG
# should be resolved here and then passed to resources in this module.

data "aws_kms_alias" "global" {
  name = "alias/${var.namespace}/${var.environment}/global"
}

data "aws_security_group" "tunnel" {
  tags = {
    Environment = var.environment
    Namespace   = var.namespace
    Name        = "${var.namespace}-${var.environment}-ec2-jump-host-security-group"
  }
}

data "aws_vpc" "this" {
  tags = {
    Environment = var.environment
    Namespace   = var.namespace
  }
}

data "aws_subnets" "private" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.this.id]
  }

  tags = {
    Environment = var.environment
    Namespace   = var.namespace
    Scope       = "private"
  }
}
