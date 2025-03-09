"""Templatetag for sanitizing alt image text."""

import re

from django import template

register = template.Library()
extension = re.compile(r'(\.(?:jpeg|jpg|png|gif))')


@register.filter
def sanitize_alt_text(text):
    text = extension.sub('', text)
    text = text.replace('_', ' ')
    text = text.capitalize()
    if not text.endswith('.'):
        text += '.'
    return text
