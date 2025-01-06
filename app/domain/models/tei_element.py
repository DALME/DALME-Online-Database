"""Models related to the use of TEI encoding."""

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q, UniqueConstraint, options

from app.abstract import TrackingMixin, UuidMixin

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')

ELEMENT_TYPES = (
    ('W', 'Word enclosing element'),
    ('S', 'Stand-alone element'),
)

MENU_SECTIONS = (
    ('annotation', 'Annotation'),
    ('editorial', 'Editorial'),
    ('formatting', 'Formatting'),
    ('layout', 'Layout'),
    ('marks', 'Marks'),
    ('other', 'Other'),
)


class ElementSet(UuidMixin, TrackingMixin):
    """Stores groups of TEI elements associated with projects or users."""

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.CharField(max_length=36, db_index=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    elements = models.ManyToManyField('domain.Element')
    is_default = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['content_type', 'object_id', 'is_default'],
                condition=Q(is_default=True),
                name='unique_is_default',
            )
        ]


class Element(UuidMixin, TrackingMixin):
    """Stores TEI element information."""

    label = models.CharField(max_length=55)
    kind = models.CharField(max_length=1, choices=ELEMENT_TYPES)
    section = models.CharField(max_length=55, choices=MENU_SECTIONS)
    description = models.TextField()
    kb_reference = models.CharField(max_length=255, null=True, blank=True)
    tag = models.CharField(max_length=55)
    compound = models.BooleanField(default=False)
    placeholder = models.CharField(max_length=255, null=True, blank=True)


class ElementAttribute(TrackingMixin):
    """Stores TEI element attribute information."""

    element = models.ForeignKey('domain.Element', on_delete=models.CASCADE)
    label = models.CharField(max_length=255)
    value = models.CharField(max_length=55)
    kind = models.CharField(max_length=55)
    description = models.TextField(null=True, blank=True)
    required = models.BooleanField(default=False)
    editable = models.BooleanField(default=False)
    default = models.CharField(max_length=55, null=True, blank=True)
    options = models.ForeignKey('domain.OptionsList', on_delete=models.SET_NULL, null=True)
