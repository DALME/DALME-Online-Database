# Entrypoint for the secret module.
#
resource "random_password" "this" {
  length           = var.length
  special          = true
  min_special      = var.min_special
  override_special = var.override_special
  # https://registry.terraform.io/providers/hashicorp/random/latest/docs#resource-keepers
  keepers = var.keepers
}

locals {
  # TODO: We should use variable cross-validation to simplify this check...
  # If var.username_password_pair and not var.username then fail validation.
  is_username_password_pair = var.username_password_pair == true && var.username != null
  random_secret             = random_password.this.result
}

locals {
  secret_string = local.is_username_password_pair ? jsonencode(zipmap([var.username_key, var.password_key], [var.username, local.random_secret])) : local.random_secret
}

resource "aws_secretsmanager_secret" "this" {
  name                    = module.secret_label.id
  description             = var.description
  kms_key_id              = var.kms_key_arn
  recovery_window_in_days = var.recovery_window

  dynamic "replica" {
    for_each = var.region != null ? { render = true } : {}

    content {
      kms_key_id = var.kms_key_arn
      region     = var.region
    }
  }

  tags = module.secret_label.tags
}

resource "aws_secretsmanager_secret_version" "this" {
  secret_id     = aws_secretsmanager_secret.this.id
  secret_string = local.secret_string
}
