"""Templatetag for returning highlights in search results."""

from django import template

register = template.Library()


@register.filter
def get_highlights(meta, context):  # noqa: C901,PLR0912
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
                                highlights.append(
                                    {'field': f'Folio {hit.folio}', 'fragment': fragment, 'link': hit.folio},
                                )
                    except AttributeError:
                        pass
    return highlights
