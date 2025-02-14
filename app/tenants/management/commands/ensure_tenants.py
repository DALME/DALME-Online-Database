"""Management command to ensure all app tenants exist for a deployment."""

import structlog

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import DataError

from tenants.models import Domain, Tenant

logger = structlog.get_logger(__name__)


class Command(BaseCommand):
    """Define the ensure_tenants command."""

    help = 'Create application tenant records.'

    def handle(self, *args, **options):  # noqa: ARG002
        """Create application tenant records."""
        # tenants = settings.TENANTS()
        tenants = {
            'IDA': {
                'domain': 'ida.ocp.systems',
                'name': 'IDA',
                'schema_name': 'public',
                'is_primary': True,
                'tenant_type': settings.TenantTypes.PUBLIC,
            },
            'DALME': {
                'domain': 'dalme.ocp.systems',
                'name': 'DALME',
                'schema_name': 'dalme',
                'is_primary': False,
                'tenant_type': settings.TenantTypes.PROJECT,
            },
            'PHARMACOPEIAS': {
                'domain': 'pharmacopeias.ocp.systems',
                'name': 'Pharmacopeias',
                'schema_name': 'pharmacopeias',
                'is_primary': False,
                'tenant_type': settings.enantTypes.PROJECT,
            },
        }

        for tenant in tenants:
            domain, name, schema_name, is_primary, tenant_type = tenant.value

            if not Tenant.objects.filter(name=name).exists():
                tenant_obj = Tenant.objects.create(
                    name=name,
                    schema_name=schema_name,
                    tenant_type=tenant_type.value,
                )
                # the dev environment needs multiple domains to run previews in the CMS
                # so the domain prop is a list, otherwise, the domain prop is a string,
                # here we turn it into a list so we can use the same logic for creating the records
                if not settings.IS_DEV:
                    domain = [domain]

                for dom in domain:
                    domain_obj = Domain.objects.create(
                        domain=dom,
                        tenant=tenant_obj,
                        is_primary=is_primary,
                    )
                    logger.info(
                        'Tenant created',
                        tenant=tenant_obj,
                        domain=domain_obj,
                    )
            else:
                # if we're in the dev environment, we only need to check the first domain
                if settings.IS_DEV:
                    domain = domain[0]

                if not Tenant.objects.filter(domains__domain=domain).exists():
                    msg = 'Invalid existing tenant record for this environment'
                    logger.error(msg, tenant=name, domain=domain)
                    raise DataError(msg)

                logger.info(
                    'Existing tenant found for domain',
                    tenant=name,
                    domain=domain,
                )
