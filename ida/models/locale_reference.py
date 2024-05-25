"""Locale reference model."""

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import options

from ida.models.templates import IntIdMixin, TrackedMixin

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class LocaleReference(IntIdMixin, TrackedMixin):
    """Stores information about geographic locales."""

    name = models.CharField(max_length=255)
    administrative_region = models.CharField(max_length=255)
    country = models.ForeignKey('ida.CountryReference', on_delete=models.SET_NULL, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    as_attribute_value = GenericRelation(
        'ida.AttributeValueFkey',
        content_type_field='target_content_type',
        object_id_field='target_id',
        related_query_name='locale',
    )

    class Meta:
        ordering = ['country', 'name']
        unique_together = ('name', 'administrative_region')

    def __str__(self):
        return f'{self.name}, {self.administrative_region}, {self.country!s}'

    def get_url(self):
        """Return url for instance."""
        return f'/locales/{self.id}'
