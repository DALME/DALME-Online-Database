"""Templatetag to return date range for a collection."""

from django import template

register = template.Library()


@register.simple_tag()
def collection_date_range(collection):
    try:
        years = sorted(collection.record_collection.get_time_coverage(published=True).keys())
        return f'{years[0]} - {years[-1]}' if len(years) > 1 else f'{years[0]}+'
    except (IndexError, AttributeError):
        return 'Unknown'
