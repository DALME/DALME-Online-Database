"""Mixin that allows attributes to be attached to a model instance."""

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import Case, Exists, ExpressionWrapper, OuterRef, Subquery, When

from ida.models.attribute import Attribute

from .attribute_field import AttributeField


class AttributesQueryset(models.QuerySet):
    def as_manager(cls):  # noqa: N805
        manager = AttributesManager.from_queryset(cls)()
        manager._built_with_as_manager = True  # noqa: SLF001
        return manager

    as_manager.queryset_only = True
    as_manager = classmethod(as_manager)

    def include_attrs(self, *args):
        for attr in args:
            attr_sq = Attribute.objects.filter(
                **{f'ida_{self.model.__name__.lower()}_related': OuterRef('pk'), 'attribute_type__name': attr}
            )
            qs = self.annotate(
                **{
                    attr: ExpressionWrapper(
                        Case(When(Exists(attr_sq), then=Subquery(attr_sq.values_list('value', flat=True)[:1]))),
                        output_field=AttributeField(),
                    )
                }
            )
        return qs


class AttributesManager(models.Manager):
    def get_queryset(self):
        return AttributesQueryset(self.model, using=self._db)

    def include_attrs(self, *args):
        qs = self.get_queryset()
        for attr in args:
            attr_sq = Attribute.objects.filter(
                **{f'ida_{qs.model.__name__.lower()}_related': OuterRef('pk'), 'attribute_type__name': attr}
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


class AttributeMixin(models.Model):
    attributes = GenericRelation(
        'ida.Attribute',
        related_query_name='%(app_label)s_%(class)s_related',
    )

    objects = AttributesManager()

    class Meta:
        abstract = True

    @property
    def attribute_count(self):
        """Return count of attributes."""
        return self.attributes.count()
