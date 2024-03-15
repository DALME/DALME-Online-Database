"""Templatetag to return source details."""

from django import template

from public.serializers import RecordSerializer

register = template.Library()


@register.simple_tag(takes_context=True)
def get_source_details(context):
    page = context['page']
    source = page.source
    source_set = page.source_set
    result = {}

    if source:
        data = RecordSerializer(source).data
        result.update(
            {
                'source': source,
                'name': data['name'],
                'short_name': data['short_name'],
                'date': data.get('date'),
                'locale': data.get('locale'),
                'language': data.get('language'),
                'url': f'/collections/records/{source.pk}/',
            },
        )

    if source_set:
        result.update(
            {
                'source_set': source_set,
                'collection_url': f"/collections/{source_set.name.replace(' ', '-').lower()}/",
            },
        )

    return result if result else None
