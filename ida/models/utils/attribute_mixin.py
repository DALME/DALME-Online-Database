"""Mixin that allows attributes to be attached to a model instance."""

from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Case, Exists, ExpressionWrapper, OuterRef, Subquery, When

from ida.models.attribute import Attribute

from .attribute_field import AttributeField


class IncludeAttributesQueryset(models.QuerySet):
    def include_attrs(self, *args):
        qs = self.prefetch_related('attributes')
        for attr in args:
            attr_sq = Attribute.objects.filter(
                **{f'ida_{self.model.__name__.lower()}_related': OuterRef('pk'), 'attribute_type__name': attr}
            )
            qs = qs.annotate(
                **{
                    attr: ExpressionWrapper(
                        Case(When(Exists(attr_sq), then=Subquery(attr_sq.values_list('value', flat=True)[:1]))),
                        output_field=AttributeField(),
                    )
                }
            )
        return qs


class FullAttributesManager(models.Manager):
    def get_queryset(self):
        model = self.model
        qs = IncludeAttributesQueryset(model, using=self._db)
        ct = ContentType.objects.get_for_model(model)
        if hasattr(ct, 'contenttypeextended'):
            model_fields = [i.name for i in model._meta.get_fields()]  # noqa: SLF001
            attribute_list = [
                i
                for i in ct.contenttypeextended.attribute_types.exclude(is_local=True).values_list('name', flat=True)
                if i not in model_fields
            ]
            qs = qs.include_attrs(*attribute_list)
        return qs


class AttributeMixin(models.Model):
    attributes = GenericRelation(
        'ida.Attribute',
        related_query_name='%(app_label)s_%(class)s_related',
    )

    objects = IncludeAttributesQueryset.as_manager()
    att_objects = FullAttributesManager()

    class Meta:
        abstract = True

    @property
    def attribute_count(self):
        """Return count of attributes."""
        return self.attributes.count()
