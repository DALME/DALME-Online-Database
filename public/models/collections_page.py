"""Model collections page data."""

from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.contrib.routable_page.models import route

from django.template.response import TemplateResponse

from public.extensions.bibliography.models import CitableMixin
from public.extensions.gradients.models import GradientMixin
from public.models.base_page import BasePage
from public.models.search_enabled_page import SearchEnabled
from public.models.settings import Settings


class Collections(SearchEnabled, CitableMixin, GradientMixin):
    parent_page_types = ['public.Home']
    subpage_types = [
        'public.Collection',
        'public.Flat',
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
