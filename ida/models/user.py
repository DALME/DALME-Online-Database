"""Model user and profile data."""

import humps

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import options
from django.urls import reverse

from ida.tenant import get_current_tenant

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
    """Override the default User model."""

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name='user_set',
        related_query_name='user',
    )

    def save(self, *args, **kwargs):
        """Override the save method to populate additional user data.

        We do this here rather than in a signal because we want to make sure
        the process is atomic (which is indeed true within save but not for a
        signal, by default).

        """
        # Capture this here before it mutates during super().save().
        created = self._state.adding
        super().save(*args, **kwargs)
        if created:
            Profile.objects.create(user=self)
            tenant = get_current_tenant()
            if bool(tenant):  # This just checks the proxy is actually bound to a value.
                tenant.members.add(self)


class Profile(models.Model):
    """One-to-one extension of user model.

    Accomodate additional user related data, including permissions of
    associated accounts on other platforms.

    """

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=50, blank=True)
    preferences = models.JSONField(default=get_default_preferences)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        """Return instance absolute url."""
        return reverse('user_detail', kwargs={'username': self.user.username})

    @property
    def profile_image(self):
        """Return url to avatar image."""
        try:
            avatar = self.user.wagtail_userprofile.avatar
        except ObjectDoesNotExist:
            return None
        return settings.MEDIA_URL + str(avatar) if avatar else None
