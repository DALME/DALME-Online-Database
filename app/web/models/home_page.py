"""Model home page data."""

from datetime import datetime

from wagtail.admin.panels import FieldPanel

from django.db import models
from django.utils import timezone

from web.extensions.banners.models import Banner
from web.extensions.gradients.models import GradientMixin
from web.models.base_page import BasePage
from web.models.featured_essay_page import Essay
from web.models.featured_inventory_page import FeaturedInventory
from web.models.featured_object_page import FeaturedObject


class Home(BasePage, GradientMixin):
    template = 'web/home.html'

    learn_more_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='The page that should open when "Learn more..." is selected.',
    )
    subpage_types = [
        'web.Section',
        'web.Features',
        'web.Collections',
    ]

    metadata_panels = [
        *GradientMixin.metadata_panels,
        FieldPanel('learn_more_page'),
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
