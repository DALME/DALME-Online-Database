"""Project model."""

from django.db import models
from django.db.models import options

from ida.models.abstract import TrackingMixin
from ida.models.tenant import Tenant

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class Project(TrackingMixin):
    """Stores information about projects."""

    name = models.CharField(max_length=55)
    description = models.TextField(blank=True, null=True)
    zotero_library_id = models.IntegerField(
        null=True,
        verbose_name='Zotero library ID',
        help_text='Group ID for Zotero library to use for this project.',
    )
    zotero_api_key = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Zotero API key',
        help_text="Zotero API key granting access to project's library.",
    )
    tenant = models.OneToOneField(Tenant, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return f'{self.name} ({self.id})'
