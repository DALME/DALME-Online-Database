"""Mixin for tracking activity with user ids and timestamps."""

from django_currentuser.middleware import get_current_user

from django.conf import settings
from django.db import models


class TrackingMixin(models.Model):
    creation_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        default=get_current_user,
        related_name='%(app_label)s_%(class)s_creation',
        null=True,
    )
    modification_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        default=get_current_user,
        related_name='%(app_label)s_%(class)s_modification',
        null=True,
    )
    creation_timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modification_timestamp = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True

    def class_name(self):
        """Return specific model class name."""
        return self.__class__.__name__
