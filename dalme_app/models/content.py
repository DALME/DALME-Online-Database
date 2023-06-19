from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import options

from dalme_app.models.templates import dalmeIntid

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class ContentTypeExtended(dalmeIntid):
    """Extends ContentType to store extra information."""

    content_type = models.OneToOneField(
        ContentType,
        on_delete=models.CASCADE,
        related_name='extended',
        null=True,
    )
    name = models.CharField(max_length=255, unique=True)
    short_name = models.CharField(max_length=55)
    description = models.TextField()
    is_abstract = models.BooleanField(default=True)
    attribute_types = models.ManyToManyField('AttributeType', through='ContentAttributeTypes')
    parents = models.ManyToManyField('ContentTypeExtended', related_name='children')
    can_view = models.BooleanField(default=True)
    can_edit = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)
    can_add = models.BooleanField(default=False)
    can_remove = models.BooleanField(default=False)

    def __str__(self):  # noqa: D105
        return self.name

    class Meta:  # noqa: D106
        ordering = ['id']


class ContentAttributeTypes(dalmeIntid):
    """Links attribute types with content types and stores related metadata."""

    content_type = models.ForeignKey(
        'ContentTypeExtended',
        to_field='id',
        db_index=True,
        on_delete=models.CASCADE,
        related_name='attribute_type_list',
    )
    attribute_type = models.ForeignKey(
        'AttributeType',
        to_field='id',
        db_index=True,
        on_delete=models.CASCADE,
        related_name='content_types',
    )
    order = models.IntegerField(db_index=True, null=True)
    required = models.BooleanField(default=False)
    unique = models.BooleanField(default=True)
    options_override = models.ForeignKey('OptionsList', on_delete=models.SET_NULL, null=True)
    label_override = models.CharField(max_length=255, blank=True)
    description_override = models.TextField(blank=True)

    class Meta:  # noqa: D106
        unique_together = ('content_type', 'attribute_type')
