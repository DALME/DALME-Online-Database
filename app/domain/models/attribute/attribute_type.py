"""Attribute type model."""

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import MultipleObjectsReturned
from django.db import models

from domain.models.abstract import DATA_TYPES, TrackingMixin


class AttributeType(TrackingMixin):
    """Stores attribute definitions."""

    name = models.CharField(max_length=55, unique=True)
    label = models.CharField(max_length=255)
    description = models.TextField()
    data_type = models.CharField(max_length=15, choices=DATA_TYPES)
    is_local = models.BooleanField(default=False)
    source = models.CharField(max_length=255, blank=True, null=True)
    same_as = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    options = models.ForeignKey('domain.OptionsList', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name

    def get_options_for_content(self, content):
        """Return options for attribute type and content."""
        if not content:
            return self.options

        try:
            ctype = ContentType.objects.get_for_model(content)
        except AttributeError:
            try:
                ctype = ContentType.objects.get(model=content)
            except (ContentType.DoesNotExist, MultipleObjectsReturned):
                try:
                    ctype = ContentType.objects.get(contenttypeextended__name=content)
                except (ContentType.DoesNotExist, MultipleObjectsReturned):
                    return self.options

        qs = self.attribute_type.contenttypes.filter(content_type=ctype.id)
        override_options = qs.first().override_options if qs.exists() else None
        return override_options if override_options else self.options
