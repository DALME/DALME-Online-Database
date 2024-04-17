"""Model home page data."""

from datetime import datetime

from wagtail.admin.panels import FieldPanel, FieldRowPanel
from wagtail.fields import StreamField

from django.db import models
from django.utils import timezone

from public.blocks import SponsorBlock
from public.extensions.banners.models import Banner
from public.extensions.gradients.models import Gradient
from public.models.base_page import BasePage
from public.models.featured_essay_page import Essay
from public.models.featured_inventory_page import FeaturedInventory
from public.models.featured_object_page import FeaturedObject


class Home(BasePage):
    template = 'home.html'

    gradient = models.ForeignKey(
        Gradient,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='The gradient to be used over the header image.',
    )
    learn_more_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='The page that should open when "Learn more..." is selected.',
    )

    sponsors = StreamField([('sponsors', SponsorBlock())], null=True)

    subpage_types = [
        'public.Section',
        'public.Features',
        'public.Collections',
    ]

    content_panels = [
        *BasePage.content_panels,
        FieldRowPanel(
            [
                FieldPanel('header_image'),
                FieldPanel('gradient'),
            ],
            heading='Header',
        ),
        FieldPanel('learn_more_page'),
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

        today = datetime.now(tz=timezone.get_current_timezone()).date()
        context['banners'] = Banner.objects.filter(
            start_date__lte=today,
            end_date__gte=today,
        ).order_by('start_date')

        return context
