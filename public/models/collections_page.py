"""Model collections page data."""

from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.contrib.routable_page.models import route

from django.db import models
from django.template.response import TemplateResponse

from public.models.base_page import BasePage
from public.models.search_enabled_page import SearchEnabled
from public.models.settings import Settings


class Collections(SearchEnabled):
    citable = models.BooleanField(
        default=True,
        help_text='Check this box to show the "Cite" menu for this page.',
    )
    gradient = models.ForeignKey(
        'public.Gradient',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    parent_page_types = ['public.Home']
    subpage_types = [
        'public.Collection',
        'public.Flat',
    ]

    content_panels = [
        *BasePage.content_panels,
        FieldPanel('header_image'),
        FieldPanel('header_position'),
        FieldPanel('gradient'),
        FieldPanel('short_title'),
        FieldPanel('citable'),
        FieldPanel('body'),
        MultiFieldPanel([InlinePanel('corpora', min_num=1, label='Corpus')], heading='Corpora'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context['corpora'] = [(corpus, corpus.collections.all()) for corpus in self.corpora.all()]
        return context

    @route(r'^explore/$', name='explore')
    def explore(self, request):
        context = self.get_context(request)

        context.update(
            {
                'header_image': Settings.objects.first().explore_header_image,
                'header_position': Settings.objects.first().explore_header_position,
                'explore': True,
            },
        )

        return TemplateResponse(
            request,
            'public/explore.html',
            context,
        )
