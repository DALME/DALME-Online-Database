# Instantiate the orchestration module.

terraform {
  source = "../../../..//modules/infra/orchestration/"
}

locals {
  env           = read_terragrunt_config(find_in_parent_folders("environment.hcl"))
  ports         = local.env.locals.ports
  spot_provider = "FARGATE_SPOT"
}

# Valid Fargate CPU/memory combinations
# -------------------------------------
# CPU value       Memory value (MiB)
# 256 (.25 vCPU)  512 (0.5GB), 1024 (1GB), 2048 (2GB)
# 512 (.5 vCPU)   1024 (1GB), 2048 (2GB), 3072 (3GB), 4096 (4GB)
# 1024 (1 vCPU)   2048 (2GB), 3072 (3GB), 4096 (4GB), 5120 (5GB), 6144 (6GB), 7168 (7GB), 8192 (8GB)
# 2048 (2 vCPU)   Between 4096 (4GB) and 16384 (16GB) in increments of 1024 (1GB)
# 4096 (4 vCPU)   Between 8192 (8GB) and 30720 (30GB) in increments of 1024 (1GB)

inputs = {
  capacity_providers = [local.spot_provider]
  default_capacity_provider_strategy = {
    base              = 1
    weight            = 100
    capacity_provider = local.spot_provider
  }
  postgres_port = local.ports.postgres
  proxy_port    = local.ports.proxy
}
