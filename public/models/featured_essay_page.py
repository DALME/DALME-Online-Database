"""Model featured essay page data."""

from public.extensions.records.models import record_mixin_factory
from public.models.featured_page import FeaturedPage

RecordClass = record_mixin_factory()


class Essay(FeaturedPage, RecordClass):
    short_title = 'Essay'
    parent_page_types = ['public.Features']
    subpage_types = []
    page_description = 'A page suitable for short to medium essays. Can link to records or collections.'
    template = 'public/feature.html'

    metadata_panels = [
        *FeaturedPage.metadata_panels,
        *RecordClass.metadata_panels,
    ]

    class Meta:
        verbose_name = 'Essay'
        verbose_name_plural = 'Essays'
