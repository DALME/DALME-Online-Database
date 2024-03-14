"""Define model templates.

These mixins and utilities are used to more easily associate common data points
with system data models; things like timestamps and unique IDs.

"""

import os
import uuid

from django_currentuser.middleware import get_current_user

from django.conf import settings
from django.db import models


def get_current_username():
    """Return current user's name."""
    return get_current_user().username


class IDABasic(models.Model):
    """Model template with timestamps, but no pre-defined ID or Owner."""

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
        return self.__class__.__name__


class IDAUuid(IDABasic):
    """Model template with a unique ID assigned by `uuid.uuid4`, resulting in a long, random identifier."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)

    class Meta:
        abstract = True


class IDAIntid(IDABasic):
    """Model template with a unique ID assigned as a sequential integer."""

    id = models.AutoField(primary_key=True, unique=True, db_index=True)

    class Meta:
        abstract = True


class IDAOwned(IDABasic):
    """Model template with an owner field."""

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
