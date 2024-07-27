# Entrypoint for the cloudfront module.

locals {
  # TODO: So we only need to slice this because we want to keep the ida in the
  # tenants so to make this more portable we should just do it one level up and
  # pass it in, then it's a bit more flexible.
  additional_domains        = slice(var.additional_domains, 1, length(var.additional_domains))
  wildcard_domains          = [for domain in var.additional_domains : "*.${domain}"]
  subject_alternative_names = concat(local.additional_domains, local.wildcard_domains)
  zone_ids = {
    for zone in data.aws_route53_zone.tenant_zones : zone.name => zone.zone_id
  }
}

resource "aws_acm_certificate" "cloudfront" {
  domain_name               = var.domain
  subject_alternative_names = local.subject_alternative_names
  validation_method         = "DNS"

  lifecycle {
    create_before_destroy = true
  }

  tags = module.cloudfront_certificate_label.tags
}

resource "aws_route53_record" "cloudfront" {
  for_each = {
    for dvo in aws_acm_certificate.cloudfront.domain_validation_options : dvo.domain_name => {
      name    = dvo.resource_record_name
      record  = dvo.resource_record_value
      type    = dvo.resource_record_type
      zone_id = local.zone_ids[dvo.domain_name]
    } if !strcontains(dvo.domain_name, "*.")
  }

  allow_overwrite = true
  name            = each.value.name
  records         = [each.value.record]
  ttl             = var.dns_ttl
  type            = each.value.type
  zone_id         = each.value.zone_id
}

resource "aws_acm_certificate_validation" "cloudfront" {
  certificate_arn = aws_acm_certificate.cloudfront.arn
  validation_record_fqdns = [
    for record in aws_route53_record.cloudfront : record.fqdn
  ]
}

# Cloudfront is a complicated resource and here I've just abstracted it to the
# extent that we are actually using that functionality. Should we need to start
# using anything else it has to offer then this definition can be extended to
# cover those needs.
resource "aws_cloudfront_distribution" "this" {
  aliases             = var.aliases
  default_root_object = var.default_root_object
  enabled             = true
  is_ipv6_enabled     = true
  price_class         = var.price_class
  wait_for_deployment = true
  web_acl_id          = var.web_acl_id

  # Cloudfront will fail on create unless the certificates are validated.
  depends_on = [
    aws_acm_certificate_validation.cloudfront
  ]

  logging_config {
    bucket          = var.log_destination
    prefix          = "cloudfront"
    include_cookies = false
  }

  dynamic "origin" {
    for_each = var.origin

    content {
      domain_name              = origin.value.domain_name
      origin_id                = origin.value.origin_id
      origin_access_control_id = try(origin.value.origin_access_control_id, null)

      dynamic "custom_origin_config" {
        for_each = try(origin.value.custom_origin_config, null) == null ? [] : [origin.value.custom_origin_config]
        iterator = c

        content {
          http_port              = c.value.http_port
          https_port             = c.value.https_port
          origin_protocol_policy = c.value.origin_protocol_policy
          origin_ssl_protocols   = c.value.origin_ssl_protocols
        }
      }

      dynamic "custom_header" {
        for_each = try(origin.value.custom_header, [])

        content {
          name  = custom_header.value.name
          value = custom_header.value.value
        }
      }
    }
  }

  dynamic "default_cache_behavior" {
    for_each = [var.default_cache_behavior]
    iterator = i

    content {
      allowed_methods        = i.value.allowed_methods
      cache_policy_id        = try(i.value.cache_policy_id, null)
      cached_methods         = i.value.cached_methods
      compress               = try(i.value.compress, null)
      target_origin_id       = i.value.target_origin_id
      viewer_protocol_policy = i.value.viewer_protocol_policy

      default_ttl = try(i.value.default_ttl, null)
      min_ttl     = try(i.value.min_ttl, null)
      max_ttl     = try(i.value.max_ttl, null)

      dynamic "forwarded_values" {
        for_each = try(i.value.forwarded_values, null) != null && try(i.value.cache_policy_id, null) == null ? [true] : []

        content {
          query_string            = try(i.value.forwarded_values.query_string, false)
          query_string_cache_keys = try(i.value.forwarded_values.query_string_cache_keys, [])
          headers                 = try(i.value.forwarded_values.headers, [])

          cookies {
            forward           = try(i.value.forwarded_values.cookies.forward, "none")
            whitelisted_names = try(i.value.forwarded_values.cookies.whitelisted_names, null)
          }
        }
      }

      dynamic "lambda_function_association" {
        for_each = try(i.value.lambda_function_association, [])
        iterator = l

        content {
          event_type   = l.key
          lambda_arn   = l.value.lambda_arn
          include_body = try(l.value.include_body, null)
        }
      }

      dynamic "function_association" {
        for_each = try(i.value.function_association, [])
        iterator = f

        content {
          event_type   = f.key
          function_arn = f.value.function_arn
        }
      }
    }
  }

  dynamic "ordered_cache_behavior" {
    for_each = var.ordered_cache_behavior
    iterator = i

    content {
      allowed_methods        = i.value.allowed_methods
      cache_policy_id        = try(i.value.cache_policy_id, null)
      cached_methods         = i.value.cached_methods
      compress               = try(i.value.compress, null)
      path_pattern           = i.value.path_pattern
      target_origin_id       = i.value.target_origin_id
      viewer_protocol_policy = i.value.viewer_protocol_policy

      default_ttl = try(i.value.default_ttl, null)
      min_ttl     = try(i.value.min_ttl, null)
      max_ttl     = try(i.value.max_ttl, null)

      dynamic "forwarded_values" {
        for_each = try(i.value.forwarded_values, null) != null && try(i.value.cache_policy_id, null) == null ? [true] : []

        content {
          query_string            = try(i.value.forwarded_values.query_string, false)
          query_string_cache_keys = try(i.value.forwarded_values.query_string_cache_keys, [])
          headers                 = try(i.value.forwarded_values.headers, [])

          cookies {
            forward           = try(i.value.forwarded_values.cookies.forward, "none")
            whitelisted_names = try(i.value.forwarded_values.cookies.whitelisted_names, null)
          }
        }
      }

      dynamic "lambda_function_association" {
        for_each = try(i.value.lambda_function_association, [])
        iterator = l

        content {
          event_type   = l.key
          lambda_arn   = l.value.lambda_arn
          include_body = try(l.value.include_body, null)
        }
      }

      dynamic "function_association" {
        for_each = try(i.value.function_association, [])
        iterator = f

        content {
          event_type   = f.key
          function_arn = f.value.function_arn
        }
      }
    }
  }

  restrictions {
    dynamic "geo_restriction" {
      for_each = [var.geo_restriction]

      content {
        restriction_type = try(geo_restriction.value.restriction_type, "none")
        locations        = try(geo_restriction.value.locations, [])
      }
    }
  }

  viewer_certificate {
    acm_certificate_arn      = aws_acm_certificate.cloudfront.arn
    minimum_protocol_version = "TLSv1.2_2021"
    ssl_support_method       = "sni-only"
  }

  tags = module.cloudfront_label.tags
}
