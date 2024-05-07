"""User-related models."""

import humps
from wagtail.users.models import UserProfile

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q, options
from django.urls import reverse

from ida.context import get_current_tenant

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


def get_default_preferences(camelize=True):
    """Define the default preferences for a user profile."""
    preferences = {
        'general': {
            'tooltips_on': True,
            'sidebar_collapsed': False,
        },
        'source_editor': {
            'font_size': '14',
            'highlight_word': True,
            'show_guides': True,
            'show_gutter': True,
            'show_invisibles': False,
            'show_lineNumbers': True,
            'soft_wrap': True,
            'theme': 'Chrome',
        },
    }
    return humps.camelize(preferences) if camelize else preferences


class User(AbstractUser):
    """Override the default auth User model."""

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
            # self.profile = Profile(full_name=f'{self.first_name} {self.last_name}')
            super().save(*args, **kwargs)

            # Add the new user to the current tenant.
            tenant = get_current_tenant()
            if bool(tenant):  # This just checks the proxy is actually bound to a value.
                tenant.members.add(self)
        else:
            super().save(*args, **kwargs)


class Profile(UserProfile):
    """Extends the Wagtail UserProfile model to add additional user related data."""

    full_name = models.CharField(max_length=50, blank=True)
    preferences = models.JSONField(default=get_default_preferences)

    def __str__(self):
        return self.user.get_username()

    def get_absolute_url(self):
        """Return instance absolute url."""
        return reverse('user_detail', kwargs={'username': self.user.username})

    @property
    def profile_image(self):
        """Return url to avatar image."""
        return settings.MEDIA_URL + str(self.avatar) if self.avatar else None
