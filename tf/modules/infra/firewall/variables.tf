# Variables for the firewall module.

variable "countries" {
  description = "A list of country codes for scoping geo rules."
  type        = list(string)
}

variable "force_destroy" {
  description = "Whether deletion protection is active on the logging buckets."
  type        = bool
}

variable "ipv4_ip_set_addresses" {
  description = "IPV4 format addresses for the firewall."
  type        = list(string)
}

variable "ipv6_ip_set_addresses" {
  description = "IPV6 format addresses for the firewall."
  type        = list(string)
}

variable "lifecycle_rule" {
  description = "Configuration for the logging bucket lifecycle."
  type = object({
    expiration_days            = number,
    noncurrent_expiration_days = number,
    noncurrent_transition_days = number,
    storage_class              = string,
  })
  default = {
    expiration_days            = 90,
    noncurrent_expiration_days = 90,
    noncurrent_transition_days = 30,
    storage_class              = "STANDARD_IA",
  }
}

variable "rules" {
  description = "Data for settings parameters in the rule declarations."
  type = object({
    domestic_dos_limit = number,
    global_dos_limit   = number,
  })
}
