# Data sources for the load-balancer module.
#
# Any dependencies between this node and ancestors on the environment DAG
# should be resolved here and then passed to resources in this module.

data "aws_vpc" "this" {
  tags = {
    Environment = var.environment
    Namepsace   = var.namespace
  }
}

data "aws_subnets" "public" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.this.id]
  }

  tags = {
    Environment = var.environment
    Namespace   = var.namespace
    Scope       = "public"
  }
}
