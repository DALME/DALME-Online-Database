from django import template

register = template.Library()


@register.simple_tag
def get_source_date(source):
    dates = {
        attr.attribute_type.short_name: attr
        for attr in source.attributes.all()
        if attr.attribute_type.short_name in ('start_date', 'end_date')
    }
    start_date = dates.get('start_date', '')
    end_date = dates.get('end_date', '')
    if not start_date and not end_date:
        return 'No date'
    if start_date and end_date:
        return f'{start_date} to {end_date}'
    return str(start_date) or str(end_date)


@register.simple_tag
def get_source_type(source):
    try:
        return next(
            str(attr) for attr in source.attributes.all()
            if attr.attribute_type.short_name == 'record_type'
        )
    except StopIteration:
        return ''


@register.simple_tag
def source_has_transcription(source):
    return any(
        source_page.transcription
        for source_page in source.source_pages_set.all()
    )


@register.simple_tag
def source_has_image(source):
    return any(
        source_page.page.dam_id
        for source_page in source.source_pages_set.all()
    )
