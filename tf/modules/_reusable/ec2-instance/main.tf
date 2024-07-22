# Entrypoint for the ec2-instance module.

resource "aws_security_group" "this" {
  count = var.create_security_group ? 1 : 0

  description = "Security group for the ec2 instance."
  name_prefix = "${module.ec2_label_sg.name}-"
  vpc_id      = var.vpc_id

  lifecycle {
    create_before_destroy = true
  }

  tags = module.ec2_label_sg.tags
}

locals {
  default_security_group_id = aws_security_group.this[0].id
}

resource "aws_launch_template" "this" {
  name_prefix            = "${module.ec2_label.name}-"
  image_id               = data.aws_ami.this.id
  instance_type          = var.instance_type
  update_default_version = var.update_default_version

  monitoring {
    enabled = var.monitoring
  }

  # NOTE: There are multiple options here, we can add any as they become needed.
  # https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/launch_template#network-interfaces
  dynamic "network_interfaces" {
    for_each = var.network_interfaces
    iterator = ni

    content {
      associate_public_ip_address = ni.value.associate_public_ip_address
      delete_on_termination       = ni.value.delete_on_termination
      security_groups             = try(ni.value.security_groups, [local.default_security_group_id])
      subnet_id                   = try(ni.value.subnet_id, null)
    }
  }

  iam_instance_profile {
    name = var.iam_instance_profile_name
  }

  metadata_options {
    http_endpoint               = var.metadata_options.http_endpoint
    http_tokens                 = "required"
    http_put_response_hop_limit = var.metadata_options.http_put_response_hop_limit
    http_protocol_ipv6          = try(var.metadata_options.http_protocol_ipv6, null)
    instance_metadata_tags      = var.metadata_options.instance_metadata_tags
  }

  lifecycle {
    create_before_destroy = true
  }

  tag_specifications {
    resource_type = "instance"
    tags          = module.ec2_label.tags
  }

  tag_specifications {
    resource_type = "volume"
    tags          = module.ec2_label.tags
  }

  tags = module.ec2_label.tags
}
