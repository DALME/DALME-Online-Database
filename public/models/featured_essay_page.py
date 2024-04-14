"""Model featured essay page data."""

from wagtail.admin.panels import FieldPanel

from django.db import models

from ida.models import Collection, Record
from public.models.base_page import BasePage
from public.models.common import SetFieldPanel
from public.models.featured_page import FeaturedPage


class Essay(FeaturedPage):
    short_title = 'Essay'
    source = models.ForeignKey(
        Record,
        related_name='essays',
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
    )
    source_set = models.ForeignKey(
        Collection,
        related_name='essays',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text='Optional, select a particular public set for the source associated with this essay. The source must be a member of the set chosen or the page will not validate.',
    )

    parent_page_types = ['public.Features']
    subpage_types = []
    page_description = 'A page suitable for short to medium essays. Can link to records or collections.'
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
        verbose_name = 'Essay'
        verbose_name_plural = 'Essays'
