"""Model featured object page data."""

from wagtail.admin.panels import FieldPanel

from public.extensions.records.models import record_mixin_factory
from public.models.featured_page import FeaturedPage

RecordClass = record_mixin_factory(blank=False)


class FeaturedObject(FeaturedPage, RecordClass):
    short_title = 'Object'
    parent_page_types = ['public.Features']
    subpage_types = []
    page_description = 'A page suitable for short essays built around an object. Can link to records or collections.'
    template = 'public/feature.html'

    content_panels = [
        *FeaturedPage.content_panels,
        *RecordClass.content_panels,
        FieldPanel('body'),
    ]

    class Meta:
        verbose_name = 'Object'
        verbose_name_plural = 'Objects'
