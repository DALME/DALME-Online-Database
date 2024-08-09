# Variables for the cdn module.
#
variable "force_destroy" {
  description = "Whether deletion protection is active on buckets."
  type        = bool
}

variable "default_root_object" {
  description = "The object to return (for example, index.html) the root URL is requested."
  type        = string
  default     = null
}

variable "dns_ttl" {
  description = "Time to live for the certificate DNS record."
  type        = number
}

variable "domain" {
  description = "The origin of the service."
  type        = string
}

variable "price_class" {
  description = "Selects the price class for the distribution."
  type        = string
}

variable "tenant_domains" {
  description = "Domain names per application tenant."
  type        = list(string)
}
