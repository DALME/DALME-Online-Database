"""Templatetag to return record details."""

from django import template

from api.resources.records import RecordSerializer
from domain.models import Record

register = template.Library()


@register.simple_tag(takes_context=True)
def get_record_details(context):
    page = context['page']
    record = Record.objects.include_attrs('record_type', 'description', 'locale', 'language', 'date').get(
        pk=page.record.id
    )
    record_collection = page.record_collection
    result = {}

    if record:
        data = RecordSerializer(record, field_set=['web', 'web_detail']).data
        result.update(
            {
                'record': record,
                'name': data.get('name'),
                'short_name': data.get('short_name'),
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
