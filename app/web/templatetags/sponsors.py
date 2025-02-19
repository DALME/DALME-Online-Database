"""Templatetag to return sponsors for home page."""

from django import template

from web.models import Sponsor

register = template.Library()


@register.inclusion_tag('web/includes/sponsors.html', takes_context=True)
def sponsors(context):
    return {
        'sponsors': Sponsor.objects.all(),
        'request': context['request'],
    }
