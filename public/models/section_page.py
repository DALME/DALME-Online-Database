"""Model section page data."""

from wagtail.admin.panels import FieldPanel

from django.db import models

from public.extensions.gradients.models import Gradient
from public.models.base_page import BasePage


class Section(BasePage):
    gradient = models.ForeignKey(
        Gradient,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    parent_page_types = ['public.Home']
    subpage_types = [
        'public.Flat',
        'public.Bibliography',
    ]
    page_description = 'Defines a menu section. Can have a gradient (used by child pages), but no other content.'

    content_panels = [
        *BasePage.content_panels,
        FieldPanel('short_title'),
        FieldPanel('gradient'),
    ]
