# Variables for the orchestration module.

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

variable "postgres_port" {
  description = "Port for making PostgreSQL connections."
  type        = number
}

variable "proxy_port" {
  description = "Reverse proxy listening port."
  type        = number
}
