"""Model reference data."""

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import options

from ida.models.templates import IDAIntid, IDAUuid

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class AttributeReference(IDAUuid):
    """Stores information about the provenance of attribute definitions."""

    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=55)
    description = models.TextField()
    data_type = models.CharField(max_length=15)
    source = models.CharField(max_length=255)
    term_type = models.CharField(max_length=55, blank=True)


class CountryReference(IDAIntid):
    """Stores country information."""

    name = models.CharField(max_length=255, unique=True)
    alpha_3_code = models.CharField(max_length=3)
    alpha_2_code = models.CharField(max_length=2)
    num_code = models.IntegerField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_url(self):
        """Return url for instance."""
        return f'/countries/{self.id}'


class LanguageReference(IDAIntid):
    """Stores information about languages and dialects."""

    glottocode = models.CharField(max_length=25, unique=True)
    iso6393 = models.CharField(
        max_length=25,
        unique=True,
        null=True,
        blank=True,
        default=None,
    )
    name = models.CharField(max_length=255)
    is_dialect = models.BooleanField(default=False)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    as_attribute_value = GenericRelation(
        'ida.AttributeValueFkey',
        content_type_field='target_content_type',
        object_id_field='target_id',
        related_query_name='language',
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_url(self):
        """Return url for instance."""
        return f'/languages/{self.id}'


class LocaleReference(IDAIntid):
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
