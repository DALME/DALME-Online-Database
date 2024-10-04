# Data sources for the ida module.

locals {
  cluster_key     = "ecs-cluster"
  oidc_rsa_secret = "OIDC-RSA-PRIVATE-KEY"
  secret_prefix   = "${var.namespace}-${var.environment}-secret"
}

data "aws_db_instance" "postgres" {
  db_instance_identifier = "${var.namespace}-${var.environment}-rds-postgres-${var.postgres_version}"

  tags = {
    Environment = var.environment
    Namespace   = var.namespace
  }
}

data "aws_ecs_cluster" "this" {
  cluster_name = "${var.namespace}-${var.environment}-${local.cluster_key}"

  tags = {
    Environment = var.environment
    Namespace   = var.namespace
  }
}

# The aws_cloudfront_distribution data source won't work without already
# knowing the id to filter it with and it's the only argument accepted (not
# sure what the point of that is), so we need to use an escape hatch to get
# that data from AWS via the CLI itself.
# https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/cloudfront_distribution.html
data "external" "cloudfront" {
  program = ["bash", "${path.module}/files/cloudfront.sh"]
}

data "aws_opensearch_domain" "this" {
  domain_name = "${var.namespace}-${var.environment}-opensearch"
}

data "aws_kms_alias" "global" {
  name = "alias/${var.namespace}/${var.environment}/global"
}

data "aws_lb_target_group" "this" {
  tags = {
    Environment = var.environment
    Namespace   = var.namespace
    Name        = "${var.namespace}-${var.environment}-alb-target-group"
  }
}

data "aws_s3_bucket" "staticfiles" {
  bucket = "${var.namespace}-${var.environment}-staticfiles-${var.aws_account}"
}

data "aws_security_group" "ecs" {
  tags = {
    Name        = "${var.namespace}-${var.environment}-${local.cluster_key}-security-group"
    Namespace   = var.namespace
    Environment = var.environment
  }
}

# This secret is 'unmanaged' (ie. needs to be created and populated manually)
# because there is no truly secure way for us to generate an RSA key pair via
# Terraform. Note the double '--' separator, which is correct, and how the
# admin should name the secret whenever get around to creating it.
data "aws_secretsmanager_secret_version" "oidc_rsa_key" {
  secret_id = "${local.secret_prefix}-${local.oidc_rsa_secret}--${var.unmanaged_suffix}"
}

data "aws_secretsmanager_secret_version" "opensearch_master_user" {
  secret_id = "${local.secret_prefix}-${var.opensearch_master_user_secret_name}"
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

data "aws_vpc" "this" {
  tags = {
    Environment = var.environment
    Namespace   = var.namespace
  }
}
