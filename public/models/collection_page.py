"""Model collection page data."""

from urllib import parse

from wagtail.admin.panels import FieldPanel, FieldRowPanel

from django.db import models

from ida.models import Collection
from public.extensions.bibliography.models import CitableMixin
from public.models.search_enabled_page import SearchEnabled


class Collection(SearchEnabled, CitableMixin):
    source_set = models.ForeignKey(
        Collection,
        related_name='public_collections',
        on_delete=models.PROTECT,
    )
    citable = models.BooleanField(
        default=True,
        help_text='Check this box to show the "Cite" menu for this page.',
    )
    preview = models.BooleanField(
        default=False,
        help_text='Check this box to set this collection to Preview mode only. It will be made public but not added to the search or map. Only people with the link will be able to access it.',
    )
    parent_page_types = ['public.Collections']
    subpage_types = ['public.Flat']
    page_description = 'Provides a landing page for a collection of records.'

    content_panels = [
        *SearchEnabled.content_panels,
        *CitableMixin.content_panels,
        FieldRowPanel(
            [
                FieldPanel('record_collection', classname='col8'),
                FieldPanel('preview', classname='col4'),
            ],
            heading='Collection',
        ),
        FieldPanel('body'),
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
                'records': self.source_set.member_count(),
                'languages': self.source_set.get_languages(),
                'coverage': self.source_set.get_time_coverage(),
            }
        else:
            stats_dict = {
                'records': self.source_set.member_count(published=True),
                'languages': self.source_set.get_languages(published=True),
                'coverage': self.source_set.get_time_coverage(published=True),
            }

        meta = self.source_set.attributes.filter(attribute_type__name='collection_metadata')
        if meta.exists():
            stats_dict['other'] = meta.first().value

        return stats_dict

    @property
    def count(self):
        return self.source_set.member_count(published=True)

    @property
    def sources(self):
        return self.source_set.members.all()

    def clean(self):
        if self.source_set:
            self.slug = self.source_set.name.replace(' ', '-').lower()
        return super().clean()
