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
  name = "${var.namespace}-${var.environment}-alb-security-group"

  tags = {
    Environment = var.environment
    Namespace   = var.namespace
  }
}

data "aws_security_group" "postgres" {
  name = "${var.namespace}-${var.environment}-rds-postgres-security-group"

  tags = {
    Environment = var.environment
    Namespace   = var.namespace
  }
}
