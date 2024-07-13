"""Comments model."""

import textwrap

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import options

from ida.models.abstract import TrackingMixin
from ida.models.tenant import TenantMixin

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class Comment(TenantMixin, TrackingMixin):
    content_object = GenericForeignKey('content_type', 'object_id')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.CharField(max_length=55, db_index=True)
    body = models.TextField(blank=True)

    @property
    def snippet(self):
        body_snippet = textwrap.shorten(self.body, width=35, placeholder='...')
        return f'{self.creation_user.username} - {body_snippet}...'

    def __str__(self):
        return self.snippet

    class Meta:
        ordering = ['creation_timestamp']
