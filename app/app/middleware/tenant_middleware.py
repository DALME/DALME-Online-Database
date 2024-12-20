"""Parse the tenant from the request and set the schema path."""

import structlog
from django_tenants.utils import (
    get_public_schema_name,
    get_public_schema_urlconf,
    get_tenant_types,
    has_multi_type_tenants,
    remove_www,
)

from django.conf import settings
from django.core.exceptions import DisallowedHost
from django.db import connection
from django.urls import set_urlconf

from domain.models import Domain


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
        except Domain.DoesNotExist as exc:
            msg = f'Tenant not found for: {origin}'
            raise DisallowedHost(msg) from exc

        request.tenant = domain.tenant
        connection.set_tenant(request.tenant)

        # https://github.com/django-tenants/django-tenants/blob/3305e48e62036388a4ff6f7af37277d6614fdcb5/django_tenants/middleware/main.py#L63
        public_schema_name = get_public_schema_name()
        if has_multi_type_tenants():
            tenant_types = get_tenant_types()
            if not hasattr(request, 'tenant') or (
                (request.tenant.schema_name == get_public_schema_name())
                and 'URLCONF' in tenant_types[public_schema_name]
            ):
                request.urlconf = get_public_schema_urlconf()
            else:
                tenant_type = request.tenant.get_tenant_type()
                request.urlconf = tenant_types[tenant_type]['URLCONF']
            set_urlconf(request.urlconf)

        elif hasattr(settings, 'PUBLIC_SCHEMA_URLCONF') and (request.tenant.schema_name == get_public_schema_name()):
            request.urlconf = settings.PUBLIC_SCHEMA_URLCONF

        structlog.contextvars.bind_contextvars(
            tenant=request.tenant.name,
            domain=origin,
        )

        return self.get_response(request)
