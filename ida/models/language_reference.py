"""Language reference model."""

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import options

from ida.models.templates import IDAIntid

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


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
