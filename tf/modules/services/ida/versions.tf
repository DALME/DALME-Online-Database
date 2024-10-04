# Providers for the ida module.

terraform {
  required_version = "~> 1.6"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.59.0"
    }

    external = {
      source  = "hashicorp/external"
      version = "2.3.4"
    }
  }
}
