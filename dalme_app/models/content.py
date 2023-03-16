"""Model content data."""
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import options

from dalme_app.models.templates import dalmeIntid

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class ContentTypeExtended(ContentType):
    """Extends ContentType to store extra information."""

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    is_abstract = models.BooleanField(default=True)
    attribute_types = models.ManyToManyField('AttributeType', through='ContentAttributes')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    can_view = models.BooleanField(default=True)
    can_edit = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)
    can_add = models.BooleanField(default=False)
    can_remove = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


class ContentAttributes(dalmeIntid):
    """Links attribute types with content types and stores related metadata."""

    content_type = models.ForeignKey(
        'ContentTypeExtended',
        db_index=True,
        on_delete=models.CASCADE,
        related_name='attributes_list',
    )
    attribute_type = models.ForeignKey(
        'AttributeType',
        db_index=True,
        on_delete=models.CASCADE,
        related_name='contenttypes',
    )
    is_required = models.BooleanField(default=False)
    is_unique = models.BooleanField(default=True)
    override_label = models.CharField(max_length=255, blank=True)
    override_description = models.TextField(blank=True)
    override_options = models.ForeignKey('OptionsList', on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ('content_type', 'attribute_type')
