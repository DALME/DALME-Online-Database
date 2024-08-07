# Data sources for the orchestration module.
#
# Any dependencies between this node and ancestors on the environment DAG
# should be resolved here and then passed to resources in this module.

data "aws_vpc" "this" {
  tags = {
    Environment = var.environment
    Namespace   = var.namespace
  }
}

data "aws_security_group" "alb" {
  tags = {
    Name        = "${var.key}-alb-security-group-${var.environment}"
    Environment = var.environment
    Namespace   = var.namespace
  }
}

data "aws_security_group" "postgres" {
  tags = {
    Name        = "${var.key}-rds-postgres-security-${var.environment}"
    Environment = var.environment
    Namespace   = var.namespace
  }
}
