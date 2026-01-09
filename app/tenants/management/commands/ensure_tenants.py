"""Management command to ensure all app tenants exist for a deployment."""

import structlog

from django.conf import settings
from django.core.management.base import BaseCommand

from tenants.models import Domain, Tenant

logger = structlog.get_logger(__name__)


class Command(BaseCommand):
    """Define the ensure_tenants command."""

    help = 'Create application tenant records.'

    def handle(self, *args, **options) -> None:  # noqa: ARG002
        """Create application tenant records."""
        tenants = settings.TENANTS()

        for tenant in tenants:
            domain, name, schema_name, is_primary, tenant_type = tenant.value

            qs = Tenant.objects.filter(name=name)
            if not qs.exists():
                tenant_obj = Tenant.objects.create(
                    name=name,
                    schema_name=schema_name,
                    tenant_type=tenant_type.value,
                )
                domain_obj = Domain.objects.create(
                    domain=domain,
                    tenant=tenant_obj,
                    is_primary=is_primary,
                )
                logger.info(
                    'Tenant created',
                    tenant=tenant_obj,
                    domain=domain_obj,
                )

            else:
                logger.info(
                    'Existing tenant found for domain',
                    tenant=name,
                    domain=domain,
                )
                existing_tenant = qs.first()

                # Let's catch a couple of conditions. This is highly unlikely
                # to ever happen but we'll encode for the sake of future
                # beings.
                if existing_tenant.name != name:
                    msg = "Don't mutate existing tenant names, they should be write-once/immutable."
                    raise ValueError(msg)

                if existing_tenant.schema_name != schema_name:
                    msg = "Don't mutate existing schema names, they should be write-once/immutable."
                    raise ValueError(msg)

                # You can update domain names though, if necessary. This is
                # useful if staging origins need to be altered.
                if existing_tenant.domain != domain:
                    existing_tenant.domain = domain
                    existing_tenant.save()
                    logger.info(
                        'Updated tenant domain record.',
                        tenant=name,
                        domain=domain,
                    )
