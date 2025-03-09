# Entrypoint for the ecr module.

locals {
  name = var.service == null ? "${var.namespace}.${var.image}" : "${var.namespace}.${var.service}.${var.image}"
}

resource "aws_ecr_repository" "this" {
  name = local.name
  # tfsec:ignore:aws-ecr-enforce-immutable-repository
  image_tag_mutability = "MUTABLE"
  force_delete         = var.force_delete

  image_scanning_configuration {
    scan_on_push = true
  }

  encryption_configuration {
    encryption_type = "KMS"
    kms_key         = var.kms_key_arn
  }

  tags = module.ecr_label.tags
}

resource "aws_ecr_lifecycle_policy" "images" {
  repository = aws_ecr_repository.this.name

  policy = jsonencode({
    rules = [
      {
        rulePriority = 1
        description  = "Retain the last N images."
        action       = { type = "expire" }
        selection = {
          tagStatus   = "any"
          countType   = "imageCountMoreThan"
          countNumber = var.retain_n
        }
      }
    ]
  })
}
