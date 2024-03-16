"""Templatetag to make variable from settings accessible."""

from django import template
from django.conf import settings

register = template.Library()

# only make a limited, preselected number of variables accessible
whitelist = settings.INCLUDE_IN_TEMPLATETAG


@register.simple_tag
def settings_val(name):
    if name in whitelist:
        return getattr(settings, name, '')
    return None
