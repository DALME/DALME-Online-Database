"""Model project data."""

from django.db import models
from django.db.models import options

from ida.models.templates import IDAIntid
from ida.models.tenant import Tenant

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class Project(IDAIntid):
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


class ZoteroCollection(IDAIntid):
    """Stores information about Zotero collections associated with a project."""

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='zoter_collections')
    zotero_id = models.CharField(max_length=25, help_text='Zotero ID of the collection.')
    label = models.CharField(max_length=255, help_text='Label for the collection.')
    has_biblio_sources = models.BooleanField(
        default=False,
        verbose_name='Contains sources?',
        help_text='Indicates if entries in this collection should be included as potential sources for records.',
    )

    def __str__(self):
        return f'{self.label} ({self.zotero_id})'
