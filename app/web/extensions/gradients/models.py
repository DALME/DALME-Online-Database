"""Model gradient data."""

from wagtail.admin.panels import FieldPanel, FieldRowPanel
from wagtail.models import Page

from django.db import models


class Gradient(models.Model):
    id = models.AutoField(primary_key=True, unique=True, db_index=True)
    colour_1 = models.CharField(max_length=9)
    colour_2 = models.CharField(max_length=9)
    angle = models.CharField(max_length=3)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.gradient_as_html()

    @property
    def css(self):
        return f'linear-gradient({self.angle!s}deg, {self.colour_1} 0%, {self.colour_2} 100%)'

    def gradient_as_html(self):
        return f'<div class="gradient-cell"><div style="background: {self.css}"></div></div>'

    gradient_as_html.short_description = 'Gradient'


class GradientMixin(models.Model):
    gradient = models.ForeignKey(
        Gradient,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='A gradient to overlay on the image.',
    )

    metadata_panels = [
        *Page.content_panels,
        FieldRowPanel(
            [
                FieldPanel('header_image', classname='col4'),
                FieldPanel('gradient', classname='col4'),
                FieldPanel('header_position', classname='col4'),
            ],
            heading='Header',
            classname='field-row-panel with-gradient',
            icon='bandage',
        ),
    ]

    class Meta:
        abstract = True
