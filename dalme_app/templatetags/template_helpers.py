from django import template
from dalme_app.utils import round_timesince

register = template.Library()


@register.simple_tag
def relative_url(value, field_name, urlencode=None):
    url = '?{}={}'.format(field_name, value)
    if urlencode:
        querystring = urlencode.split('&')
        filtered_querystring = filter(lambda p: p.split('=')[0] != field_name, querystring)
        encoded_querystring = '&'.join(filtered_querystring)
        url = '{}&{}'.format(url, encoded_querystring)
    return url


@register.filter
def htimesince(d):
    return round_timesince(d)


@register.simple_tag
def dict_key_lookup(_dict, key):
    # Try to fetch from the dict, and if it's not found return an empty string.
    return _dict.get(key, '')


@register.filter
def dd_record_name(name, part=''):
    name_string = name.split('(')
    if part == 'loc':
        try:
            return name_string[1][:-1]
        except IndexError:
            return 'Archival location not available'
    return name_string[0]
