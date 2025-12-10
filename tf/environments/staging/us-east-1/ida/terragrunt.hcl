# Instantiate the ida node.

include "root" {
  path = find_in_parent_folders("root.hcl")
}

include "nodes" {
  path = "${dirname(find_in_parent_folders("root.hcl"))}/nodes/ida.hcl"
}
