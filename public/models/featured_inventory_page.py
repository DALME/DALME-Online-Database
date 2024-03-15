"""Model featured inventory page data."""

from wagtail.admin.panels import FieldPanel

from django.db import models

from ida.models import Collection, Record
from public.models.base_page import BasePage
from public.models.common import SetFieldPanel
from public.models.featured_page import FeaturedPage


class FeaturedInventory(FeaturedPage):
    short_title = 'Inventory'
    source = models.ForeignKey(
        Record,
        related_name='featured_inventories',
        on_delete=models.DO_NOTHING,
        null=True,
    )
    source_set = models.ForeignKey(
        Collection,
        related_name='featured_inventories',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text='Optional, select a particular public set for the source associated with this inventory. The source must be a member of the set chosen or the page will not validate.',
    )

    parent_page_types = ['public.Features']
    subpage_types = []
    template = 'public/feature.html'

    content_panels = [
        *BasePage.content_panels,
        FieldPanel('header_image'),
        FieldPanel('header_position'),
        FieldPanel('front_page_image'),
        FieldPanel('source'),
        SetFieldPanel('source_set'),
        FieldPanel('alternate_author'),
        FieldPanel('citable'),
        FieldPanel('body'),
    ]

    class Meta:
        verbose_name = 'Inventory'
        verbose_name_plural = 'Inventories'
