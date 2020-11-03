from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from dalme_app.models._templates import dalmeUuid
import django.db.models.options as options

options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('in_db',)


class RightsPolicy(dalmeUuid):
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
    rights = models.TextField(blank=True, default=None)
    rights_notice = models.JSONField(null=True)
    licence = models.TextField(blank=True, null=True, default=None)
    rights_holder = models.CharField(max_length=255, null=True, default=None)
    notice_display = models.BooleanField(default=False)
    public_display = models.BooleanField(default=True)
    attachments = models.ForeignKey('Attachment', blank=True, null=True, on_delete=models.SET_NULL)
    comments = GenericRelation('Comment')

    def __str__(self):
        return self.name

    def get_url(self):
        return '/rights/' + str(self.id)
