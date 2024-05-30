"""Zotero collection model."""

from django.db import models
from django.db.models import options

from ida.models.utils import TrackingMixin

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class ZoteroCollection(TrackingMixin):
    """Stores information about Zotero collections associated with a project."""

    id = models.CharField(primary_key=True, max_length=25, help_text='Zotero ID of the collection.')
    project = models.ForeignKey('ida.Project', on_delete=models.CASCADE, related_name='zotero_collections')
    label = models.CharField(max_length=255, help_text='Label for the collection.')
    has_biblio_sources = models.BooleanField(
        default=False,
        verbose_name='Contains sources?',
        help_text='Indicates if entries in this collection should be included as potential sources for records.',
    )

    def __str__(self):
        return f'{self.label} ({self.id})'
