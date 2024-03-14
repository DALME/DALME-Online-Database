"""Model rights policy data."""

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import options

from ida.models.templates import IDAUuid

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class RightsPolicy(IDAUuid):
    """Stores information about rights concerning archival images."""

    COPYRIGHTED = 1
    ORPHANED = 2
    OWNED = 3
    PUBLIC_DOMAIN = 4
    UNKNOWN = 5
    RIGHTS_STATUS = (
        (COPYRIGHTED, 'Copyrighted'),
        (ORPHANED, 'Orphaned'),
        (OWNED, 'Owned'),
        (PUBLIC_DOMAIN, 'Public Domain'),
        (UNKNOWN, 'Unknown'),
    )

    name = models.CharField(max_length=100)
    rights_status = models.IntegerField(choices=RIGHTS_STATUS, default=5)
    rights = models.TextField(blank=True)
    rights_notice = models.JSONField(null=True)
    licence = models.TextField(blank=True, null=True)
    rights_holder = models.CharField(max_length=255, blank=True)
    notice_display = models.BooleanField(default=False)
    public_display = models.BooleanField(default=True)
    attachments = models.ForeignKey('ida.Attachment', blank=True, null=True, on_delete=models.SET_NULL)
    comments = GenericRelation('ida.Comment')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_url(self):
        """Return url for instance."""
        return f'/rights/{self.id}'
