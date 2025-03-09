"""Snippet model for social media links."""

from django.db import models


class SocialMedia(models.Model):
    name = models.CharField(max_length=55, help_text='Platform/service name.')
    icon = models.CharField(max_length=255, help_text='Name of FA icon to use.')
    css_class = models.CharField(max_length=255, help_text='CSS class to apply to link.')
    url = models.URLField(
        blank=True,
        verbose_name='Website',
        help_text='URL of the service.',
    )

    class Meta:
        verbose_name_plural = 'Social media'

    def __str__(self):
        return self.name
