# Instantiate the load-balancer node.

include "root" {
  path = find_in_parent_folders()
}

include "nodes" {
  path = "${dirname(find_in_parent_folders())}/nodes/load-balancer.hcl"
}
