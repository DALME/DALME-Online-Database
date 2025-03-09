# Variables for the waf module.

variable "countries" {
  description = "A list of country codes for scoping geo rules."
  type        = list(string)
}

variable "environment" {
  description = "Identify the deployment environment."
  type        = string
}

variable "ipv4_ip_set_addresses" {
  description = "Provide addresess for a WAFv2 IP set resource in ipv4 format."
  type        = list(string)
}

variable "ipv6_ip_set_addresses" {
  description = "Provide addresess for a WAFv2 IP set resource in ipv6 format."
  type        = list(string)
}

# https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/wafv2_web_acl_logging_configuration#log_destination_configs
variable "log_destination_configs" {
  description = "Optional ARN of a resource to receive WAF logs."
  type        = string
  default     = null
}

variable "namespace" {
  description = "The project namespace."
  type        = string
}

variable "rules" {
  description = "Data for settings parameters in the rule declarations."
  type = object({
    domestic_dos_limit = number,
    global_dos_limit   = number,
  })
}

variable "service" {
  description = "An optional service namespace."
  type        = string
  default     = null
}
