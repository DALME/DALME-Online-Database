"""Base models for multitenancy scoped models.

If a model needs to be tenant-aware then it must inherit from TenantMixin.

As well as adding the foreign key to the relevant tenant row, it also overrides
the db manager so that `objects` always filters over the request tenant
transparently. If you need to see all the objects across all tenants (for a
superuser view for example) then you can fallback to the `unscoped` manager
which doesn't take multitenancy into account.

"""

import os

from django.db import models

from ida.context import get_current_tenant
from ida.models.abstract.custom_manager import CustomManager, CustomQuerySet


class TenantMixin(models.Model):
    """Mixin to make a model multitenant aware."""

    tenant = models.ForeignKey(
        'ida.Tenant',
        on_delete=models.PROTECT,
        null=False,
    )

    objects = CustomManager.from_queryset(CustomQuerySet)()
    unscoped = models.Manager()  # noqa: DJ012

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """Add tenant when saving record."""
        if not hasattr(self, 'tenant') and not os.environ.get('DATA_MIGRATION'):
            self.tenant = get_current_tenant()
        super().save(*args, **kwargs)

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.is_tenanted = True
