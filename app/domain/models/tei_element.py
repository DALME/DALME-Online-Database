"""Models related to the use of TEI encoding."""

from django.db import models
from django.db.models import Q, UniqueConstraint, options

from app.abstract import OwnedMixin, TrackingMixin, UuidMixin

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
    icon = models.CharField(max_length=255, null=True, blank=True)


class ElementAttribute(TrackingMixin):
    """Stores TEI element attribute information."""

    element = models.ForeignKey(Element, on_delete=models.CASCADE, related_name='attributes')
    label = models.CharField(max_length=255)
    value = models.CharField(max_length=55)
    kind = models.CharField(max_length=55)
    description = models.TextField(null=True, blank=True)
    required = models.BooleanField(default=False)
    editable = models.BooleanField(default=False)
    default = models.CharField(max_length=55, null=True, blank=True)
    options = models.ForeignKey('domain.OptionsList', on_delete=models.SET_NULL, null=True)


class ElementSet(UuidMixin, TrackingMixin, OwnedMixin):
    """Stores groups of TEI elements associated with projects or users."""

    label = models.CharField(max_length=55)
    description = models.TextField(null=True, blank=True)
    project = models.ForeignKey('domain.Project', on_delete=models.CASCADE, null=True)
    is_default = models.BooleanField(default=False)
    elements = models.ManyToManyField(Element, through='domain.ElementSetMembership')

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['owner', 'is_default'],
                condition=Q(is_default=True),
                name='unique_is_default',
            )
        ]


class ElementSetMembership(models.Model):
    """Join/trough model for ElementSet and Element."""

    element_set = models.ForeignKey(ElementSet, on_delete=models.CASCADE, related_name='members')
    element = models.ForeignKey(Element, on_delete=models.CASCADE)
    in_context_menu = models.BooleanField(default=False)
    in_toolbar = models.BooleanField(default=False)
    shortcut = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['element_set', 'element'],
                name='unique_association',
            )
        ]

    def __str__(self):
        return f'{self.element}->{self.element_set}'
