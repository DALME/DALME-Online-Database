import json
import pathlib

from django.conf import settings
from django.contrib.auth.models import Group, User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import options
from django.urls import reverse

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


with pathlib.Path('static/snippets/default_user_preferences.json').open() as fp:
    DEFAULT_PREFS = dict(json.load(fp))


def default_preferences():
    """Return user default preferences."""
    return DEFAULT_PREFS


class GroupProperties(models.Model):
    """Extension of group model to accomodate additional group related data."""

    ADMIN = 1
    DAM = 2
    TEAM = 3
    KNOWLEDGEBASE = 4
    WEBSITE = 5
    GROUP_TYPES = (
        (ADMIN, 'Admin'),
        (DAM, 'DAM'),
        (TEAM, 'Team'),
        (KNOWLEDGEBASE, 'Knowledge Base'),
        (WEBSITE, 'Website'),
    )

    group = models.OneToOneField(Group, on_delete=models.CASCADE, related_name='properties')
    type = models.IntegerField(choices=GROUP_TYPES)
    description = models.CharField(max_length=255)

    def __str__(self):  # noqa: D105
        return self.group.name


class Profile(models.Model):
    """Extension of user model to accomodate additional user related data."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=50, blank=True)
    primary_group = models.ForeignKey(Group, to_field='id', db_index=True, on_delete=models.SET_NULL, null=True)
    preferences = models.JSONField(default=default_preferences)

    def __str__(self):  # noqa: D105
        return self.user.username

    def get_absolute_url(self):
        """Return instance absolute url."""
        return reverse('user_detail', kwargs={'username': self.user.username})

    @property
    def profile_image(self):
        """Return url to avatar image."""
        try:
            if self.user.wagtail_userprofile.avatar is not None and self.user.wagtail_userprofile.avatar:
                return settings.MEDIA_URL + str(self.user.wagtail_userprofile.avatar)
            else:  # noqa: RET505
                return None
        except ObjectDoesNotExist:
            return None
