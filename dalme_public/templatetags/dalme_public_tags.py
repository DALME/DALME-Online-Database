from django import template

from dalme_app.serializers import SourceSerializer


register = template.Library()


# TODO: Combine these two into one call to serialize?
@register.simple_tag
def get_source_date(source):
    # try:
    #     return source.date
    # except AttributeError:
    data = SourceSerializer().to_representation(source)
    return data['attributes'].get('date')


@register.simple_tag
def get_source_type(source):
    try:
        return source.source_type
    except AttributeError:
        data = SourceSerializer().to_representation(source)
        return data['attributes'].get('record_type')


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


@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    ctx = context['request'].GET.copy()
    for key, value in kwargs.items():
        ctx[key] = value
    for key in [key for key, value in ctx.items() if not value]:
        del ctx[key]
    return ctx.urlencode()
