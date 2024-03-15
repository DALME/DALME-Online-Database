"""Templatetag to return url of features."""

from django import template

from public.models import (
    Features,
)

register = template.Library()


@register.simple_tag()
def get_features_url():
    return Features.objects.first().url
