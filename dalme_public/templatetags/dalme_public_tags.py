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

    if start_date and not end_date:
        return str(start_date)
    if end_date and not start_date:
        return str(end_date)
    if start_date == end_date:
        return str(start_date)
    if start_date and end_date:
        return f'{start_date} to {end_date}'
    return ''


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


@register.inclusion_tag('dalme_public/inclusion/_annotated_related_page.html')
def annotate_related_page(page):
    source_page = page.sources.first()
    has_transcription = (
        source_page is not None and source_page.transcription is not None
    )
    return {
        'has_image': page.dam_id is not None,
        'has_transcription': has_transcription,
    }
