"""Snippet model for sponsors."""

from django.db import models

from web.extensions.images.models import BaseImage


class Sponsor(models.Model):
    name = models.CharField(max_length=255, help_text='Name of the sponsor.')
    logo = models.ForeignKey(
        BaseImage,
        null=True,
        on_delete=models.SET_NULL,
        help_text='Logo of the sponsor.',
    )
    url = models.URLField(
        blank=True,
        verbose_name='Website',
        help_text="URL of the sponsor's website.",
    )

    def __str__(self):
        return self.name
