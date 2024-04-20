"""Templatetag to return record details."""

from django import template

from public.extensions.records.serializers import RecordSerializer

register = template.Library()


@register.simple_tag(takes_context=True)
def get_record_details(context):
    page = context['page']
    record = page.record
    record_collection = page.record_collection
    result = {}

    if record:
        data = RecordSerializer(record).data
        result.update(
            {
                'record': record,
                'name': data['name'],
                'short_name': data['short_name'],
                'date': data.get('date'),
                'locale': data.get('locale'),
                'language': data.get('language'),
                'url': f'/collections/records/{record.pk}/',
            },
        )

    if record_collection:
        result.update(
            {
                'record_collection': record_collection,
                'collection_url': f"/collections/{record_collection.name.replace(' ', '-').lower()}/",
            },
        )

    return result if result else None
