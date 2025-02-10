"""Mixin for tracking activity with user ids and timestamps."""

from django_currentuser.middleware import get_current_user

from django.conf import settings
from django.db import models
from django.utils import timezone


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
    # these have to use "default=timezone.now" instead of "auto_now_add=True" and "auto_now=True"
    # to allow timestamps to be preserved during data migrations
    # auto_now_add and auto_now *always* update the field, even if a timestamp is provided on
    # save() or create(): https://docs.djangoproject.com/en/5.1/ref/models/fields/#datefield
    creation_timestamp = models.DateTimeField(default=timezone.now, null=True, blank=True)
    modification_timestamp = models.DateTimeField(default=timezone.now, null=True, blank=True)

    class Meta:
        abstract = True

    def class_name(self):
        """Return specific model class name."""
        return self.__class__.__name__
