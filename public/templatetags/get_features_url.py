"""Templatetag to return url of features."""

from django import template

from public.models import Features

register = template.Library()


@register.simple_tag()
def get_features_url():
    feature = Features.objects.first()
    if feature:
        return feature.url
    return None
