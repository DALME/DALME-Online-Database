"""Management command to ensure all app tenant records exist."""
import structlog

from django.conf import settings
from django.core.management.base import BaseCommand

from dalme_app.models import Domain, Tenant

logger = structlog.get_logger(__name__)


class Command(BaseCommand):
    """Define the ensure_tenants command."""

    help = 'Create application tenant records.'  # noqa: A003

    def handle(self, *args, **options):  # noqa: ARG002
        """Create application tenant records."""
        for tenant in settings.TENANTS():
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
                    'Created tenant', tenant=tenant_obj, domain=domain_obj,
                )
            else:
                logger.info(
                    'Existing tenant %s found for domain: %s',
                    tenant=name,
                    domain=domain,
                )
