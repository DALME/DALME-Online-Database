"""Models for bibliography extension."""

from wagtail.admin.panels import FieldPanel

from django.db import models


class CitableMixin(models.Model):
    citable = models.BooleanField(
        default=True,
        help_text='Check this box to show the "Cite" menu for this page.',
    )

    content_panels = [
        FieldPanel('citable'),
    ]

    class Meta:
        abstract = True
