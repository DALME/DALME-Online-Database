"""Model featured essay page data."""

from web.extensions.records.models import record_mixin_factory
from web.models.featured_page import FeaturedPage

RecordClass = record_mixin_factory()


class Essay(FeaturedPage, RecordClass):
    short_title = 'Essay'
    parent_page_types = ['web.Features']
    subpage_types = []
    page_description = 'A page suitable for short to medium essays. Can link to records or collections.'
    template = 'web/feature.html'

    metadata_panels = [
        *FeaturedPage.metadata_panels,
        *RecordClass.metadata_panels,
    ]

    class Meta:
        verbose_name = 'Essay'
        verbose_name_plural = 'Essays'
