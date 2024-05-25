"""User preferences model."""

import json

from django.conf import settings
from django.db import models

from .templates import TrackedMixin, UuidMixin

DATA_TYPES = (
    ('bool', 'Boolean'),
    ('int', 'Integer'),
    ('json', 'JSON'),
    ('str', 'String'),
)


class PreferenceKey(TrackedMixin, UuidMixin):
    name = models.CharField(max_length=55, unique=True)
    label = models.CharField(max_length=255)
    description = models.TextField()
    data_type = models.CharField(choices=DATA_TYPES, max_length=4)
    group = models.CharField(max_length=55)
    default = models.TextField()


class Preference(TrackedMixin):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='preferences')
    key = models.ForeignKey(PreferenceKey, on_delete=models.CASCADE)
    data = models.TextField()

    def __str__(self):
        val = 'Object' if self.key.data_type == 'json' else self.data
        return f'{self.key.name}={val}'

    @property
    def value(self):
        match self.key.data_type:
            case 'bool':
                return self.data == 'True'
            case 'int':
                return int(self.data)
            case 'json':
                return json.loads(self.data)
            case _:
                return self.data
