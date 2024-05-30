"""Mixin for tracking instance ownership."""

import os

from django_currentuser.middleware import get_current_user

from django.conf import settings
from django.db import models


class OwnedMixin(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='%(app_label)s_%(class)s_related',
        null=True,
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """Save record with owner info."""
        defaults = {
            'force_insert': False,
            'force_update': False,
            'using': None,
            'update_fields': None,
        }

        if self._state.adding is True and not os.environ.get('DATA_MIGRATION'):
            self.owner = get_current_user()

        for key, value in defaults.items():
            if key not in kwargs:
                kwargs[key] = value

        super().save(*args, **kwargs)
