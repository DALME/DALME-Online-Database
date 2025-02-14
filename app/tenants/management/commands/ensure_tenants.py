"""Management command to ensure all app tenants exist for a deployment."""

import structlog

from django.conf import settings
from django.core.management.base import BaseCommand

from tenants.models import Domain, Tenant

logger = structlog.get_logger(__name__)


class Command(BaseCommand):
    """Define the ensure_tenants command."""

    help = 'Create application tenant records.'

    def handle(self, *args, **options):  # noqa: ARG002
        """Create application tenant records."""
        tenants = settings.TENANTS()

        for tenant in tenants:
            domain, additional_domains, name, schema_name, is_primary, tenant_type = tenant.value

            if not Tenant.objects.filter(name=name).exists():
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

                if additional_domains:
                    for additional_domain in additional_domains:
                        domain_obj = Domain.objects.create(
                            domain=additional_domain,
                            tenant=tenant_obj,
                            is_primary=is_primary,
                        )

            else:
                logger.info(
                    'Existing tenant found for domain',
                    tenant=name,
                    domain=domain,
                )
