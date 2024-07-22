# Entrypoint for the network module.

module "vpc_flow_logs" {
  source = "..//bucket/"

  acl                      = "log-delivery-write"
  aws_account              = var.aws_account
  control_object_ownership = true
  environment              = var.environment
  force_destroy            = var.force_destroy
  name                     = "logs-vpc"
  namespace                = var.namespace
  object_ownership         = "ObjectWriter"

  lifecycle_rule = [
    {
      id     = "ssm"
      status = "Enabled"

      filter = {
        prefix = "/"
      }

      expiration = {
        days = 90
      }

      noncurrent_version_expiration = {
        noncurrent_days = 90
      }

      noncurrent_version_transition = {
        noncurrent_days = 30
        storage_class   = "STANDARD_IA"
      }
    }
  ]

  server_side_encryption_configuration = {
    rule = {
      apply_server_side_encryption_by_default = {
        sse_algorithm = "AES256"
      }
      bucket_key_enabled = true
    }
  }

  versioning = {
    enabled = true
  }
}

module "vpc" {
  source = "..//vpc/"

  az_count               = var.az_count
  cidr                   = var.cidr
  destination_cidr_block = var.destination_cidr_block
  environment            = var.environment
  log_destination        = module.vpc_flow_logs.bucket_arn
  log_destination_type   = "s3"
  namespace              = var.namespace
}

module "session_manager" {
  source = "..//ssm/"

  aws_account   = var.aws_account
  environment   = var.environment
  force_destroy = var.force_destroy
  namespace     = var.namespace
}

locals {
  metadata_options = {
    http_endpoint               = "enabled",
    http_put_response_hop_limit = 1,
    instance_metadata_tags      = "enabled",
  }
  network_interfaces = [
    { associate_public_ip_address = false, delete_on_termination = true },
  ]
}

module "jump_host" {
  source = "..//ec2-instance/"

  environment               = var.environment
  iam_instance_profile_name = aws_iam_instance_profile.jump_host_profile.name
  instance_type             = "t3.nano"
  metadata_options          = local.metadata_options
  namespace                 = var.namespace
  network_interfaces        = local.network_interfaces
  vpc_id                    = module.vpc.vpc_id

  ami_filters = [
    { name = "architecture", values = ["x86_64"] }
  ]
  ami_name_regex = "^amzn2-ami-hvm.*-ebs"
}

# NOTE: AWS makes these rules by default for any security group but terraform
# disables them, so I am not sure why tfsec considers this an issue.
resource "aws_security_group_rule" "jump_host_egress_https" {
  security_group_id = module.jump_host.security_group_id
  description       = "Allow outgoing traffic to HTTPS from the jump host."
  type              = "egress"
  from_port         = var.ssl_port
  to_port           = var.ssl_port
  protocol          = "tcp"
  # tfsec:ignore:aws-ec2-no-public-egress-sgr
  cidr_blocks = ["0.0.0.0/0"]
}

# A 'self-healing' autoscaling group for the jump host that will provision a
# new server (maybe in a different AZ if necessary) if an existing host (or AZ)
# has become unavailable.
resource "aws_autoscaling_group" "jump_host" {
  name_prefix      = module.network_jh_label.name
  max_size         = 1
  min_size         = 1
  desired_capacity = 1

  vpc_zone_identifier = module.vpc.subnets.private

  default_cooldown          = 180
  health_check_grace_period = 180
  health_check_type         = "EC2"

  launch_template {
    id      = module.jump_host.launch_template_id
    version = module.jump_host.launch_template_latest_version
  }

  termination_policies = [
    "OldestLaunchConfiguration",
  ]

  instance_refresh {
    strategy = "Rolling"
  }

  tag {
    key                 = "Name"
    value               = module.network_jh_label.name
    propagate_at_launch = true
  }

  tag {
    key                 = "Environment"
    value               = var.environment
    propagate_at_launch = true
  }

  tag {
    key                 = "Namespace"
    value               = var.namespace
    propagate_at_launch = true
  }

  lifecycle {
    create_before_destroy = true
  }
}
