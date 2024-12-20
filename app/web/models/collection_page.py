"""Model collection page data."""

from urllib import parse

from wagtail.admin.panels import FieldPanel, FieldRowPanel

from django.db import models

from domain.models import Collection
from web.extensions.bibliography.models import CitableMixin
from web.models.search_enabled_page import SearchEnabled


class Collection(SearchEnabled, CitableMixin):
    record_collection = models.ForeignKey(
        Collection,
        on_delete=models.PROTECT,
        verbose_name='Collection',
        help_text='Collection to associate with this page.',
    )
    preview = models.BooleanField(
        default=False,
        help_text='Check this box to set this collection to Preview mode only.',
    )
    parent_page_types = ['web.Collections']
    subpage_types = ['web.Flat']
    page_description = 'Provides a landing page for a collection of records.'

    metadata_panels = [
        *SearchEnabled.metadata_panels,
        *CitableMixin.metadata_panels,
        FieldRowPanel(
            [
                FieldPanel('record_collection', classname='col8'),
                FieldPanel('preview', classname='col4'),
            ],
            heading='Collection',
            classname='field-row-panel',
            icon='layer-group',
            help_text='A collection in Preview mode will be made public, but not added to the search index or to the map in the Explore page. Only someone with the full url will be able to access it.',
        ),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        if request.META.get('HTTP_REFERER'):
            params = dict(parse.parse_qsl(parse.urlsplit(request.META.get('HTTP_REFERER')).query))
            if 'collection' in params:
                context['collection'] = params['collection']
        return context

    @property
    def stats(self):
        if self.preview:
            stats_dict = {
                'records': self.record_collection.member_count(),
                'languages': self.record_collection.get_languages(),
                'coverage': self.record_collection.get_time_coverage(),
            }
        else:
            stats_dict = {
                'records': self.record_collection.member_count(published=True),
                'languages': self.record_collection.get_languages(published=True),
                'coverage': self.record_collection.get_time_coverage(published=True),
            }

        meta = self.record_collection.attributes.filter(attribute_type__name='collection_metadata')
        if meta.exists():
            stats_dict['other'] = meta.first().value

        return stats_dict

    @property
    def count(self):
        return self.record_collection.member_count(published=True)

    @property
    def records(self):
        return self.record_collection.members.all()

    def clean(self):
        if self.record_collection:
            self.slug = self.record_collection.name.replace(' ', '-').lower()
        return super().clean()
