"""Parse the tenant from the request and set the schema path."""

import structlog
from django_tenants.utils import remove_www

from django.core.exceptions import DisallowedHost
from django.db import connection

from ida.models import Domain


class TenantMiddleware:
    """Identify a tenant from the request and set the db schema path."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """Invoke the middleware layer."""
        origin = remove_www(request.META['HTTP_HOST'])
        connection.set_schema_to_public()

        try:
            domain = Domain.objects.select_related('tenant').get(domain=origin)
        except Domain.DoesNotExist:
            return DisallowedHost()

        request.tenant = domain.tenant
        connection.set_tenant(request.tenant)

        structlog.contextvars.bind_contextvars(
            tenant=request.tenant.name,
            domain=origin,
        )

        return self.get_response(request)
