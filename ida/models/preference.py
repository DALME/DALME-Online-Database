"""User preferences model."""

import json

from django.conf import settings
from django.db import models

from ida.models.utils import BASE_DATA_TYPES, TrackingMixin, UuidMixin


class PreferenceKey(TrackingMixin, UuidMixin):
    name = models.CharField(max_length=55, unique=True)
    label = models.CharField(max_length=255)
    description = models.TextField()
    data_type = models.CharField(choices=BASE_DATA_TYPES, max_length=15)
    group = models.CharField(max_length=55)
    default = models.TextField()


class Preference(TrackingMixin):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='preferences')
    key = models.ForeignKey(PreferenceKey, on_delete=models.CASCADE)
    data = models.TextField()

    def __str__(self):
        val = 'Object' if self.key.data_type == 'json' else self.data
        return f'{self.key.name}={val}'

    @property
    def value(self):
        match self.key.data_type:
            case 'BOOL':
                return self.data == 'True'
            case 'INT':
                return int(self.data)
            case 'JSON':
                return json.loads(self.data)
            case _:
                return self.data
