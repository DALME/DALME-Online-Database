"""Custom model manager.

Model manager to add functionality in models that are tenant-scoped
or that use the sttributes system.

"""

import os

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.expressions import ArraySubquery
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Case, Exists, ExpressionWrapper, OuterRef, When

from app.context import get_current_tenant

from .uuid_mixin import UuidMixin

PROD_ENVS = {'staging', 'production'}


class CustomQuerySet(models.QuerySet):
    """Refine the default queryset on models managed by CustomManager."""

    def as_manager(cls):  # noqa: N805
        manager = CustomManager.from_queryset(cls)()
        manager._built_with_as_manager = True  # noqa: SLF001
        return manager

    as_manager.queryset_only = True
    as_manager = classmethod(as_manager)

    def include_attrs(self, *args):
        from domain.models.attribute import Attribute, AttributeField, AttributeType, ListField

        qs = self.prefetch_related('attributes')
        for attr in args:
            # check if we're dealing with multi-table inheritance
            # in which case we need to use the parent model
            model = self.model
            bases = model._meta.get_parent_list()  # noqa: SLF001
            if len(bases) == 1 and issubclass(bases[0], UuidMixin) and bases[0] != self.model:
                model = bases[0]

            attr_sq = Attribute.objects.filter(
                **{f'domain_{model.__name__.lower()}_related': OuterRef('pk'), 'attribute_type__name': attr}
            )
            # check if attribute is_unique
            try:
                is_unique = (
                    AttributeType.objects.get(name=attr)
                    .contenttypes.get(content_type=ContentType.objects.get_for_model(model))
                    .is_unique
                )
            except ObjectDoesNotExist:
                is_unique = True  # True is default value for is_unique

            if is_unique:
                qs = qs.annotate(**{attr: attr_sq.values_list('value', flat=True)})
            else:
                qs = qs.annotate(
                    **{
                        attr: ExpressionWrapper(
                            Case(When(Exists(attr_sq), then=ArraySubquery(attr_sq.values_list('value', flat=True)))),
                            output_field=ListField(AttributeField(), is_unique=is_unique),
                        )
                    }
                )

        return qs


class CustomManager(models.Manager):
    """Replace the default manager on all models inheriting from AttributeMixin or TenantMixin."""

    def get_queryset(self):
        """Override to return a filtered queryset."""

        def filter_tenant(qs):
            """Return a tenant-scoped queryset.

            If this throws an exeption because the tenant contextvar is unbound, it
            means either 1) we're in dev mode and we're trying to use shell_plus
            but the tenant is not set because we're outside request/response. Or 2)
            we are in staging/prod and we're running a management command in a
            container (again we're outside request/response) and any evaluation of
            scoped querysets that happens at start-up time (eg. on DRF endpoint
            definitions) will also find the tenant context unbound and throw
            RuntimeError. In those cases we just fallback to the unscoped manager.

            """
            tenant = get_current_tenant()

            try:
                return qs.filter(tenant__id=tenant.pk)
            except RuntimeError:
                if settings.DEBUG or os.environ['ENV'] in PROD_ENVS:
                    return qs.filter()
                raise

        is_tenanted = hasattr(self.model, 'is_tenanted')
        attribute_list = self.model.attribute_list() if hasattr(self.model, 'attribute_list') else None

        if self._queryset_class != models.QuerySet:
            qs = super().get_queryset()
        else:
            qs = CustomQuerySet(self.model, using=self._db)

        if is_tenanted:
            qs = filter_tenant(qs)

        if attribute_list:
            qs = qs.include_attrs(*attribute_list)

        return qs

    def unscoped(self):
        """Return a non-tenant-scoped queryset when calling a related manager."""
        queryset = models.QuerySet(self.model, using=self._db)
        return self._apply_rel_filters(queryset)
