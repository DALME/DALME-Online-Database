"""Templatetag to format the name of metrics for display."""

from django import template

register = template.Library()


@register.filter
def format_metric(metric):
    tokens = metric.split('_')
    tokens[0] = tokens[0].capitalize()
    return ' '.join(tokens)
