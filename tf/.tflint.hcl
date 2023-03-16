plugin "aws" { enabled = true }

rule "aws_resource_missing_tags" {
  enabled = true
  tags    = ["Name", "Environment", "Service"]
  exclude = []
}
