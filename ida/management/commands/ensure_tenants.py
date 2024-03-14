"""Management command to ensure all app tenants exist for a deployment."""

import structlog

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import DataError

from ida.models import Domain, Tenant

logger = structlog.get_logger(__name__)


class Command(BaseCommand):
    """Define the ensure_tenants command."""

    help = 'Create application tenant records.'

    def handle(self, *args, **options):  # noqa: ARG002
        """Create application tenant records."""
        tenants = settings.TENANTS()
        for tenant in tenants:
            domain, name, schema_name = tenant.value
            if not Tenant.objects.filter(name=name).exists():
                tenant_obj = Tenant.objects.create(
                    name=name,
                    schema_name=schema_name,
                )
                domain_obj = Domain.objects.create(
                    domain=domain,
                    tenant=tenant_obj,
                    is_primary=False,
                )
                logger.info(
                    'Tenant created',
                    tenant=tenant_obj,
                    domain=domain_obj,
                )
            else:
                if not Tenant.objects.filter(domains__domain=domain).exists():
                    msg = 'Invalid existing tenant record for this environment'
                    logger.error(msg, tenant=name, domain=domain)
                    raise DataError(msg)

                logger.info(
                    'Existing tenant found for domain',
                    tenant=name,
                    domain=domain,
                )
