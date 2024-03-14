# Terraform definitions for the ecr module.

terraform {
  required_version = "~> 1.3"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.14.0"
    }
  }
}

resource "aws_ecr_repository" "images" {
  count = length(var.images)
  name  = "${var.image}.${element(var.images, count.index)}"
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

  tags = {
    Name = "${var.image}.${element(var.images, count.index)}"
  }
}

resource "aws_ecr_lifecycle_policy" "images" {
  count      = length(var.images)
  repository = element(aws_ecr_repository.images[*].name, count.index)

  policy = jsonencode({
    rules = [
      {
        rulePriority = 1
        description  = "Keep the last 10 images."
        action       = { type = "expire" }
        selection = {
          tagStatus   = "any"
          countType   = "imageCountMoreThan"
          countNumber = 10
        }
      }
    ]
  })
}
