"""Attribute-related models."""

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import options

from app.abstract import TrackingMixin, UuidMixin
from domain.models.attribute.attribute_field import AttributeField

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class AttributeManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(
                name=models.F('attribute_type__name'),
                label=models.F('attribute_type__label'),
                description=models.F('attribute_type__description'),
                data_type=models.F('attribute_type__data_type'),
            )
        )


class Attribute(UuidMixin, TrackingMixin):
    """Stores attribute data."""

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.CharField(max_length=36, db_index=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    attribute_type = models.ForeignKey(
        'domain.AttributeType',
        db_index=True,
        on_delete=models.CASCADE,
        related_name='newattributes',
    )
    value = AttributeField(blank=False, null=False)

    objects = AttributeManager()

    class Meta:
        base_manager_name = 'objects'
        default_manager_name = 'objects'

    def __str__(self):
        return f'{self.attribute_type.name}: {self.value}'

    @property
    def is_unique(self):
        return self.attribute_type.contenttypes.get(content_type=self.content_type).is_unique

    def get_options(self):
        """Return options for attribute."""
        qs = self.attribute_type.contenttypes.filter(content_type=self.content_type.id)
        override_options = qs.first().override_options if qs.exists() else None
        return override_options if override_options else self.attribute_type.options
