"""Attribute type model."""

from django.db import models

from ida.models.utils import DATA_TYPES, TrackingMixin


class AttributeType(TrackingMixin):
    """Stores attribute definitions."""

    name = models.CharField(max_length=55, unique=True)
    label = models.CharField(max_length=255)
    description = models.TextField()
    data_type = models.CharField(max_length=15, choices=DATA_TYPES)
    is_local = models.BooleanField(default=False)
    source = models.CharField(max_length=255, blank=True, null=True)
    same_as = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    options = models.ForeignKey('ida.OptionsList', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name

    def get_options(self):
        """Return options for attribute type."""
        return self.options
