"""Model featured essay page data."""

from wagtail.admin.panels import FieldPanel

from public.extensions.records.models import record_mixin_factory
from public.models.featured_page import FeaturedPage

RecordClass = record_mixin_factory()


class Essay(FeaturedPage, RecordClass):
    short_title = 'Essay'
    parent_page_types = ['public.Features']
    subpage_types = []
    page_description = 'A page suitable for short to medium essays. Can link to records or collections.'
    template = 'public/feature.html'

    content_panels = [
        *FeaturedPage.content_panels,
        *RecordClass.content_panels,
        FieldPanel('body'),
    ]

    class Meta:
        verbose_name = 'Essay'
        verbose_name_plural = 'Essays'
