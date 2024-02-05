# Terraform definitions for the secrets module.

terraform {
  required_version = "~> 1.3"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.14.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.4"
    }
  }
}

resource "aws_kms_key" "main" {
  description         = "Global KMS key per deploy environment."
  enable_key_rotation = true
  policy              = data.aws_iam_policy_document.kms.json

  tags = {
    Name = "${var.service}-kms-key-main-${var.environment}"
  }
}

resource "random_password" "password" {
  count            = length(var.secrets)
  length           = 64
  special          = true
  min_special      = 5
  override_special = "!#$%^&*()-_=+[]{}<>:?"

  # https://registry.terraform.io/providers/hashicorp/random/latest/docs#resource-keepers
  keepers = {
    version = contains(var.static_secrets, element(var.secrets, count.index)) ? 1 : var.keeper
  }
}

resource "aws_secretsmanager_secret" "secrets" {
  count                   = length(var.secrets)
  name                    = "${var.service}-secret-${var.environment}-${element(var.secrets, count.index)}"
  kms_key_id              = aws_kms_key.main.arn
  recovery_window_in_days = var.recovery_window

  tags = {
    Name = "${var.service}-secret-${var.environment}-${element(var.secrets, count.index)}"
  }
}

resource "aws_secretsmanager_secret_version" "secrets_values" {
  count         = length(var.secrets)
  secret_id     = element(aws_secretsmanager_secret.secrets[*].id, count.index)
  secret_string = element(random_password.password[*].result, count.index)
}
