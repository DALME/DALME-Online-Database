"""Model collections page data."""

from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.contrib.routable_page.models import path

from django.template.response import TemplateResponse

from web.extensions.bibliography.models import CitableMixin
from web.extensions.gradients.models import GradientMixin
from web.models.base_page import BasePage
from web.models.search_enabled_page import SearchEnabled
from web.models.settings import Settings


class Collections(SearchEnabled, CitableMixin, GradientMixin):
    template = 'web/collections.html'
    parent_page_types = ['web.Home']
    subpage_types = [
        'web.Collection',
        'web.Flat',
    ]
    page_description = 'The "Collections" landing page.'

    metadata_panels = [
        *GradientMixin.metadata_panels,
        *CitableMixin.metadata_panels,
        FieldPanel('short_title'),
    ]

    content_panels = [
        *BasePage.content_panels,
        MultiFieldPanel([InlinePanel('corpora', min_num=1, label='Corpus')], heading='Corpora'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context['corpora'] = [(corpus, corpus.collections.all()) for corpus in self.corpora.all()]
        return context

    @path('explore/', name='explore')
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
            'explore.html',
            context,
        )
