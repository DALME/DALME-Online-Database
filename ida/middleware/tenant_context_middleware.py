"""Define the tenant context middleware."""

import contextvars

from werkzeug.local import LocalProxy

from django.conf import settings
from django.core.exceptions import DisallowedHost

_tenant = contextvars.ContextVar('tenant')
TENANT = LocalProxy(_tenant)


class TenantContextMiddleware:
    """Identify a registered tenant from a request and expose it to the app.

    We also override any settings that need to be dynamic over tenants.

    The contextvar is just a convenience so we can always access the tenant in
    places without always having to thread through a value from the request.

    Must be run after the django-tenants TenantMainMiddleware so the tenant
    is already present as an attribute on the request object.

    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """Invoke the middleware layer."""
        try:
            domain = request.tenant.domains.first().domain
        except AttributeError:
            return DisallowedHost()

        settings.CSRF_COOKIE_DOMAIN = f'.{domain}'
        settings.SESSION_COOKIE_DOMAIN = f'.{domain}'
        settings.WAGTAIL_SITE_NAME = request.tenant.name

        token = _tenant.set(request.tenant)

        response = self.get_response(request)

        _tenant.reset(token)

        return response
