"""Views for public app."""

from wagtail.admin.panels import FieldPanel
from wagtail.admin.ui.tables import UpdatedAtColumn
from wagtail.snippets.views.snippets import SnippetViewSet

from public.models import FooterLink, SocialMedia, Sponsor


class FooterLinksViewSet(SnippetViewSet):
    model = FooterLink
    icon = 'link'
    list_display = ['label', 'page', UpdatedAtColumn()]

    panels = [
        FieldPanel('label'),
        FieldPanel('page'),
    ]


class SponsorsViewSet(SnippetViewSet):
    model = Sponsor
    icon = 'hand-holding-heart'
    list_display = ['name', 'logo', 'url', UpdatedAtColumn()]

    panels = [
        FieldPanel('name'),
        FieldPanel('logo'),
        FieldPanel('url'),
    ]


class SocialMediaViewSet(SnippetViewSet):
    model = SocialMedia
    icon = 'square-share-nodes'
    list_display = ['name', 'icon', 'css_class', 'url', UpdatedAtColumn()]

    panels = [
        FieldPanel('name'),
        FieldPanel('icon'),
        FieldPanel('css_class'),
        FieldPanel('url'),
    ]
