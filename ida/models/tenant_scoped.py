"""Base models for multitenancy scoped models.

If a model needs to be tenant-aware then it must inherit from ScopedBase.

As well as adding the foreign key to the relevant tenant row, it also overrides
the db manager so that `objects` always filters over the request tenant
transparently. If you need to see all the objects across all tenants (for a
superuser view for example) then you can fallback to the `unscoped` manager
which doesn't take multitenancy into account.

"""

import os

from django.conf import settings
from django.db import models

from ida.tenant import get_current_tenant


class ScopedQueryset(models.QuerySet):
    """Refine the default queryset on models managed by ScopedManager."""

    def as_manager(cls):  # noqa: N805
        manager = ScopedManager.from_queryset(cls)()
        manager._built_with_as_manager = True  # noqa: SLF001
        return manager

    as_manager.queryset_only = True

    as_manager = classmethod(as_manager)


class ScopedManager(models.Manager):
    """Replace the default manager on all models inheriting from ScopedBase."""

    def get_queryset(self):
        """Filter a tenant aware queryset.

        If this throws an exeption because the tenant contextvar is unbound, it
        means either 1) we're in dev mode and we're trying to use shell_plus
        but the tenant is not set because we're outside request/response. Or 2)
        we are in staging/prod and we're running a management command in a
        container (again we're outside request/response) and any evaluation of
        scoped querysets that happens at start-up time (eg. on DRF endpoint
        definitions) will also find the tenant context unbound and throw
        RuntimeError. In those cases we just fallback to the unscoped manager.

        """
        prod_envs = {'staging', 'production'}
        tenant = get_current_tenant()

        if self._queryset_class != models.QuerySet:
            try:
                return super().get_queryset().filter(tenant__id=tenant.pk)
            except RuntimeError:
                if settings.DEBUG or os.environ['ENV'] in prod_envs:
                    return super().get_queryset().filter()
                raise

        try:
            return ScopedQueryset(
                self.model,
                using=self._db,
            ).filter(tenant__id=tenant.pk)
        except RuntimeError:
            if settings.DEBUG or os.environ.get('ENV') in prod_envs:
                return ScopedQueryset(self.model, using=self._db).filter()
            raise


class ScopedBase(models.Model):
    """Mixin to make a model multitenant aware."""

    tenant = models.ForeignKey(
        'ida.Tenant',
        on_delete=models.PROTECT,
        null=False,
    )

    objects = ScopedManager()
    unscoped = models.Manager()  # noqa: DJ012

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """Add tenant when saving record."""
        if not hasattr(self, 'tenant') and not os.environ.get('DATA_MIGRATION'):
            self.tenant = get_current_tenant()
        super().save(*args, **kwargs)
