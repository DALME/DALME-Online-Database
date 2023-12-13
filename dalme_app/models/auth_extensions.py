"""Model extended auth data."""
import json
import pathlib

from django.contrib.auth.models import Group
from django.db import models
from django.db.models import options

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')

with pathlib.Path('static/snippets/default_user_preferences.json').open() as fp:
    DEFAULT_PREFS = dict(json.load(fp))


def default_preferences():
    """Return user default preferences."""
    return DEFAULT_PREFS


class GroupProperties(models.Model):
    """One-to-one extension of group model.

    Accomodates additional group related data, including group types.

    """

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
    group_type = models.IntegerField(choices=GROUP_TYPES)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.group.name
