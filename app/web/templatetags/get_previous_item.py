"""Templatetag to return the previous item in a for loop."""

from django import template

register = template.Library()


@register.filter
def get_previous_item(lst, current_index):
    """Return the previous item of the list using the current index if it exists."""
    current_index = int(current_index)
    if current_index == 0:
        return None
    try:
        return lst[current_index - 1]
    except IndexError:
        return None
