# Terraform outputs for the waf module.

output "waf_arn" {
  value       = aws_wafv2_web_acl.main.arn
  description = "ARN of the WAF itself."
}

output "waf_ipsets_cloudfront_ipv4_arn" {
  value       = aws_wafv2_ip_set.ipv4.arn
  description = "IPv4 blacklist ARN"
}

output "waf_ipsets_cloudfront_ipv6_arn" {
  value       = aws_wafv2_ip_set.ipv6.arn
  description = "IPv6 blacklist ARN"
}
