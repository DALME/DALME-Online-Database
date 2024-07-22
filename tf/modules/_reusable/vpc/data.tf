# Data sources for the vpc module.

# Fetch AZs in the current region.
data "aws_availability_zones" "available" {
  state = "available"
}
