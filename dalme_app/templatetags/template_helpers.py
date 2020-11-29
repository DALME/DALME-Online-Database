from django import template
from dalme_app.utils import round_timesince
from elasticsearch_dsl.utils import AttrDict

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
def get_class_name(value):
    return value.__class__.__name__


@register.filter
def htimesince(d):
    return round_timesince(d)


@register.simple_tag
def dict_key_lookup(_dict, key):
    # Try to fetch from the dict, and if it's not found return an empty string.
    return _dict.get(key, '')


@register.filter
def to_dict(target):
    if type(target) is AttrDict:
        return target.to_dict()
    if type(target) is list and type(target[0]) is tuple:
        return {i[0]: i[1] for i in target}


@register.filter
def dd_record_name(name, part=''):
    name_string = name.split('(')
    if part == 'loc':
        try:
            return name_string[1][:-1]
        except IndexError:
            return 'Archival location not available'
    return name_string[0]


@register.filter
def in_list(value, list_string):
    _list = []
    conversions = {
        'none': None,
        'blank': '',
        'empty': ' '
    }

    for item in list_string.split(','):
        if item in conversions:
            _list.append(conversions[item])
        else:
            _list.append(item)

    return value in _list


@register.filter
def get_highlights(meta, context):
    highlights = []
    if 'highlight' in meta:
        fields = list(meta.highlight.to_dict().keys())
        for field in fields:
            for fragment in meta.highlight[field]:
                try:
                    highlights.append({'field': context[field]['label'], 'fragment': fragment})

                except KeyError:
                    field_tokens = field.split('.')
                    field_tokens.pop(-1)
                    highlights.append({'field': context['.'.join(field_tokens)]['label'], 'fragment': fragment})

    if 'inner_hits' in meta:
        docs = list(meta.inner_hits.to_dict().keys())
        for doc in docs:
            for hit in meta.inner_hits[doc].hits:
                if hit.meta:
                    try:
                        fields = hit.meta.highlight.to_dict().keys()
                        for field in fields:
                            for fragment in hit.meta.highlight[field]:
                                highlights.append({'field': f'Folio {hit.folio}', 'fragment': fragment, 'link': hit.folio})

                    except AttributeError:
                        pass

    return highlights
