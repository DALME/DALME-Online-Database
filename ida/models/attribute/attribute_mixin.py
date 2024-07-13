"""Mixin that allows attributes to be attached to a model instance."""

from functools import partialmethod

from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.utils import ProgrammingError

from ida.models.abstract.custom_manager import CustomManager, CustomQuerySet


class AttributeMixin(models.Model):
    attributes = GenericRelation(
        'ida.Attribute',
        related_query_name='%(app_label)s_%(class)s_related',
    )

    objects = CustomManager.from_queryset(CustomQuerySet)()
    unattributed = models.Manager()  # noqa: DJ012

    class Meta:
        abstract = True

    def __init_subclass__(cls, **kwargs):
        """Add `attribute_list` method to subclasses."""
        super().__init_subclass__(**kwargs)

        @classmethod
        def _attribute_list(cls_or_self):
            """Return a list of non-local attribute names associated with the model."""
            try:
                ct = ContentType.objects.get_for_model(cls_or_self)
                if hasattr(ct, 'contenttypeextended'):
                    return [
                        i
                        for i in ct.contenttypeextended.attribute_types.exclude(is_local=True).values_list(
                            'name', flat=True
                        )
                        if i not in [i.name for i in cls_or_self._meta.get_fields()]  # noqa: SLF001
                    ]

            except ProgrammingError:
                return None
            return None

        cls.attribute_list = partialmethod(_attribute_list)

    @property
    def attribute_count(self):
        """Return count of attributes."""
        return self.attributes.count()
