"""Templatetag to return formatted filter url."""

from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def get_features_filter_q(context, key, value):
    params = f'?{key}={value}' if value != 'all' else ''
    for param_key, param_value in context['request'].GET.items():
        if param_key != key:
            ag = '&' if params else '?'
            params += f'{ag}{param_key}={param_value}'
    return params
