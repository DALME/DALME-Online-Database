"""Snippet model for footer links."""

from django.db import models


class FooterLink(models.Model):
    label = models.CharField(max_length=55, help_text='Label to show on the footer.')
    page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Page linked to the label.',
    )

    def __str__(self):
        return self.label
