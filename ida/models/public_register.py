"""Model public register data."""

from django_currentuser.middleware import get_current_user

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import options

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class PublicRegister(models.Model):
    """Stores information about publicly available resources."""

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.UUIDField(db_index=True, primary_key=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        default=get_current_user,
        related_name='%(app_label)s_%(class)s_creation',
        null=True,
    )
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.pk
