include "root" {
  path = find_in_parent_folders()
}

include "env-modules" {
  path = "${dirname(find_in_parent_folders())}/_env.modules/vpc.hcl"
}
