"""Test the app.middleware.tenant_context_middleware module."""

import contextvars
import sys
from unittest import mock

import pytest
from werkzeug.local import LocalProxy

from django.core.exceptions import DisallowedHost

from app.context import get_current_tenant
from tenants.middleware.tenant_context_middleware import TenantContextMiddleware
from tenants.models import Tenant


def test_get_current_tenant_fails_when_not_set():
    """Assert trying to access the current tenant context throws if unset."""
    from tenants.middleware import tenant_context_middleware

    # Explicitly reset the tenant context to simulate it not being set
    tenant_context_middleware._tenant = contextvars.ContextVar('tenant')  # noqa: SLF001
    tenant_context_middleware.TENANT = LocalProxy(tenant_context_middleware._tenant)  # noqa: SLF001
    # Patch import used by get_current_tenant
    sys.modules['tenants.middleware'].TENANT = tenant_context_middleware.TENANT

    with pytest.raises(RuntimeError) as exc:
        get_current_tenant().pk

    assert str(exc.value) == 'object is not bound'


def test_middleware_throws_if_tenant_not_on_request(rf):
    """Assert middleware fails when tenant not set."""
    request = rf.get('/', headers={'HOST': 'some.domain'})
    get_response = mock.MagicMock()
    middleware = TenantContextMiddleware(get_response)

    with pytest.raises(DisallowedHost):
        middleware(request)


@mock.patch('tenants.middleware.tenant_context_middleware._tenant')
def test_middleware(mock_ctx, rf, settings):
    """Assert the middleware sets and unsets the context correctly."""
    request = rf.get('/', headers={'HOST': 'dalme.localhost'})
    mock_tenant = mock.MagicMock(spec=Tenant)
    mock_tenant.domains.first.return_value.domain = 'dalme.localhost'
    request.tenant = mock_tenant
    request.tenant.name = 'DALME'
    get_response = mock.MagicMock()
    middleware = TenantContextMiddleware(get_response)

    middleware(request)
    tenant = get_current_tenant()

    assert settings.CSRF_COOKIE_DOMAIN == '.dalme.localhost'
    assert settings.SESSION_COOKIE_DOMAIN == '.dalme.localhost'
    assert settings.WAGTAIL_SITE_NAME == 'DALME'
    assert isinstance(tenant, LocalProxy)
    assert mock_ctx.mock_calls == [
        mock.call.set(mock_tenant),
        mock.call.reset(mock_ctx.set.return_value),
    ]
