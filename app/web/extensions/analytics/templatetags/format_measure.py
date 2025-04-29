"""Templatetag to format the name of metrics for display."""

from django import template

register = template.Library()


@register.filter
def format_measure(measure, metric):
    if metric == 'bounce_rate':
        return f'{measure}%'
    if metric == 'time_on_page':
        m, s = divmod(measure, 60)
        if m:
            return f'{m}m {s}s'
        return f'{s}s'
    return measure
