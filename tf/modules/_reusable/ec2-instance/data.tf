# Data sources for the ec2-instance module.

data "aws_ami" "this" {
  most_recent = var.ami_most_recent
  name_regex  = var.ami_name_regex
  owners      = var.ami_owners

  dynamic "filter" {
    for_each = var.ami_filters

    content {
      name   = filter.value.name
      values = filter.value.values
    }
  }
}
