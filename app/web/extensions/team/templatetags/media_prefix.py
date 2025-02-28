"""Templatetag for providing the tenanted media prefix."""

from django import template
from django.conf import settings

from app.context import get_current_tenant

register = template.Library()
tenant = get_current_tenant()


@register.simple_tag
def media_prefix():
    return f'{settings.MEDIA_URL}/{tenant}/'
