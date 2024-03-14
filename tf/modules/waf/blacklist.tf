# Blacklisted IP sets for the waf module.

resource "aws_wafv2_ip_set" "ipv4" {
  name               = "${var.service}-cloudfront-ipv4-blacklist-${var.environment}"
  scope              = "CLOUDFRONT"
  provider           = aws.acm
  ip_address_version = "IPV4"
  addresses          = ["127.0.0.1/32"]

  tags = {
    Name = "${var.service}-cloudfront-ipv4-blacklist-${var.environment}"
  }
}

resource "aws_wafv2_ip_set" "ipv6" {
  name               = "${var.service}-cloudfront-ipv6-blacklist-${var.environment}"
  scope              = "CLOUDFRONT"
  provider           = aws.acm
  ip_address_version = "IPV6"
  addresses          = ["2001:0db8:0000:0000:0000:0000:0000:0001/128"]

  tags = {
    Name = "${var.service}-cloudfront-ipv6-blacklist-${var.environment}"
  }
}
