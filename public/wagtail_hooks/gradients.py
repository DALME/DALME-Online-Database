"""Gradient snippet."""

from wagtail.admin.panels import FieldPanel
from wagtail.snippets.views.snippets import SnippetViewSet

from public.models import Gradient


class GradientViewSet(SnippetViewSet):
    model = Gradient
    icon = 'draft'
    # template_prefix = 'public/other/gradients/'
    # columns = ['Gradient']
    # list_display = ['view']

    panels = [
        FieldPanel('colour_1'),
        FieldPanel('colour_2'),
        FieldPanel('angle'),
    ]
