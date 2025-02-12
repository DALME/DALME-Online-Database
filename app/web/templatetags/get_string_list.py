"""Templatetag that returns a comma-separated string when passed a list. If an additional parameter is passed it will be used as key to extract values from a list of dictionaries."""

from django import template

register = template.Library()


@register.filter
def get_string_list(lst, params=None):
    if not lst:
        return None

    if not params:
        return ', '.join([str(i) for i in lst])

    if '|' not in params:
        return ', '.join([i[params] for i in lst])

    keys, format_str = params.split('|')

    res = []
    keys = keys.split(',') if ',' in keys else keys
    keys = [k.split('.') if '.' in k else k for k in keys]

    for key in keys:
        values = []
        for obj in lst:
            if isinstance(key, list):
                val = obj[key[0]]
                for k in key[1:]:
                    val = val[k]
                values.append(val)
            else:
                values.append(obj[key])
        res.append(values)

    return ', '.join([format_str.format(*i) for i in zip(*res, strict=False)])
