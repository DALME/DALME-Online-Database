"""Test the app.middleware.tenant_context_middleware module."""

from unittest import mock

import pytest
from werkzeug.local import LocalProxy

from django.core.exceptions import DisallowedHost

from app.context import get_current_tenant
from tenants.middleware.tenant_context_middleware import TenantContextMiddleware


def test_get_current_tenant_fails_when_not_set():
    """Assert trying to access the current tenant context throws if unset."""
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
@pytest.mark.django_db
def test_middleware(mock_ctx, rf, settings, test_domain):
    """Assert the middleware sets and unsets the context correctly."""
    request = rf.get('/', headers={'HOST': test_domain.domain})
    tenant = test_domain.tenant
    request.tenant = tenant
    get_response = mock.MagicMock()
    middleware = TenantContextMiddleware(get_response)

    middleware(request)
    set_tenant = get_current_tenant()

    assert f'.{test_domain.domain}' == settings.CSRF_COOKIE_DOMAIN
    assert f'.{test_domain.domain}' == settings.SESSION_COOKIE_DOMAIN
    assert tenant.name == settings.WAGTAIL_SITE_NAME
    assert isinstance(set_tenant, LocalProxy)
    assert mock_ctx.mock_calls == [
        mock.call.set(tenant),
        mock.call.reset(mock_ctx.set.return_value),
    ]
