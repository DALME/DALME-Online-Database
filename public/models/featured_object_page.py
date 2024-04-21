"""Model featured object page data."""

from public.extensions.records.models import record_mixin_factory
from public.models.featured_page import FeaturedPage

RecordClass = record_mixin_factory(blank=False)


class FeaturedObject(FeaturedPage, RecordClass):
    short_title = 'Object'
    parent_page_types = ['public.Features']
    subpage_types = []
    page_description = 'A page suitable for short essays built around an object. Can link to records or collections.'
    template = 'public/feature.html'

    metadata_panels = [
        *FeaturedPage.metadata_panels,
        *RecordClass.metadata_panels,
    ]

    class Meta:
        verbose_name = 'Object'
        verbose_name_plural = 'Objects'
