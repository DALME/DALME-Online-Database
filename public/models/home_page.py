"""Model home page data."""

from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField

from django.db import models

from public.blocks import (
    AnnouncementBannerBlock,
    SponsorBlock,
)
from public.models.base_page import BasePage
from public.models.featured_essay_page import Essay
from public.models.featured_inventory_page import FeaturedInventory
from public.models.featured_object_page import FeaturedObject

HEADER_POSITION = (
    ('top', 'Top'),
    ('center', 'Center'),
    ('bottom', 'Bottom'),
)


class Home(BasePage):
    template = 'home.html'

    learn_more_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    sponsors = StreamField([('sponsors', SponsorBlock())], null=True)
    banners = StreamField([('banners', AnnouncementBannerBlock())], null=True)

    subpage_types = [
        'public.Section',
        'public.Features',
        'public.Collections',
    ]

    content_panels = [
        *BasePage.content_panels,
        FieldPanel('header_image'),
        FieldPanel('learn_more_page'),
        FieldPanel('banners'),
        FieldPanel('body'),
        FieldPanel('sponsors'),
    ]

    def get_context(self, request):
        context = super().get_context(request)

        objects = FeaturedObject.objects.live().specific().order_by('go_live_at')
        inventories = FeaturedInventory.objects.live().specific().order_by('go_live_at')
        essays = Essay.objects.live().specific().order_by('go_live_at')

        context['featured_object'] = objects.last()
        context['featured_inventory'] = inventories.last()
        context['essay'] = essays.last()

        return context
