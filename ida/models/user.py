"""User-related models."""

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q, options
from django.urls import reverse

from ida.context import get_current_tenant
from ida.models.preference import Preference, PreferenceKey

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class User(AbstractUser):
    """Override the default auth User model."""

    full_name = models.CharField(max_length=255, blank=True)

    @property
    def groups_scoped(self):
        """Return the union of a user's tenant and IDA/unscoped groups.

        Note, this method will throw a RuntimeError if called outside of the
        request/response cycle.

        """
        tenant = get_current_tenant()
        q = Q(properties__tenant__pk=tenant.pk) | Q(properties__tenant__pk__isnull=True)
        return self.groups.filter(q)

    def save(self, *args, **kwargs):
        """Override the save method to populate additional user data.

        We do this here rather than in a signal because we want to make sure
        the process is atomic (which is indeed true within save but not for a
        signal, by default).

        """
        # Capture this here before it mutates during super().save().
        created = self._state.adding
        if created:
            if not self.full_name:
                self.full_name = f'{self.first_name} {self.last_name}'

            super().save(*args, **kwargs)

            # create default preferences
            preferences = [Preference(user=self, key=k, data=k.default) for k in PreferenceKey.objects.all()]
            Preference.objects.bulk_create(preferences)

            # Add the new user to the current tenant.
            # TODO: should superusers/users belonging to certain groups be added to ALL tenants?
            tenant = get_current_tenant()
            if bool(tenant):  # This just checks the proxy is actually bound to a value.
                tenant.members.add(self)
        else:
            super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Return instance absolute url."""
        return reverse('user_detail', kwargs={'username': self.user.username})

    @property
    def profile(self):
        return self.wagtail_userprofile

    @property
    def avatar_url(self):
        """Return url to avatar image."""
        return settings.MEDIA_URL + str(self.profile.avatar) if self.profile.avatar else None
