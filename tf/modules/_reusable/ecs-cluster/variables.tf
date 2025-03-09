# Variables for the ecs-cluster module.

variable "capacity_providers" {
  description = "Determine where the ECS scaling provisioning comes from."
  type        = list(string)
}

variable "default_capacity_provider_strategy" {
  description = "Tune the ECS capacity provider strategy"
  type = object({
    base              = number,
    weight            = number,
    capacity_provider = string,
  })
}

variable "environment" {
  description = "Identify the deployment environment."
  type        = string
}

variable "namespace" {
  description = "The project namespace."
  type        = string
}

variable "service" {
  description = "An optional service namespace."
  type        = string
  default     = null
}

variable "vpc_id" {
  description = "Identifier for the VPC."
  type        = string
}
