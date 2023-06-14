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
    attribute_types = models.ManyToManyField('AttributeType', through='ContentAttributeTypes')
    has_pages = models.BooleanField(default=False, db_index=True)
    has_inventory = models.BooleanField(default=False)
    parents = models.CharField(max_length=255, blank=True)
    parents_list = models.ManyToManyField('ContentTypeExtended', related_name='children')
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
    options_source = models.JSONField(null=True)
