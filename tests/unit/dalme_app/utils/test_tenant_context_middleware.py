"""Test the dalme_app.utils.tenant_context_middleware module."""
from unittest import mock

import pytest
from werkzeug.local import LocalProxy

from django.core.exceptions import DisallowedHost

from dalme_app.models import Tenant
from dalme_app.tenant import get_current_tenant
from dalme_app.utils.tenant_context_middleware import TenantContextMiddleware


def test_get_current_tenant_fails_when_not_set(mock_get_current_tenant):
    """Assert trying to access the current tenant context throws if unset."""
    # Unpatch the global mock for the getter.
    mock_get_current_tenant.side_effect = get_current_tenant

    tenant = get_current_tenant()
    with pytest.raises(RuntimeError) as exc:
        tenant.pk

    assert str(exc.value) == 'object is not bound'


def test_middleware_throws_if_tenant_not_on_request(rf):
    """Assert middleware fails when tenant not set."""
    request = rf.get('/')
    get_response = mock.MagicMock()
    middleware = TenantContextMiddleware(get_response)

    assert isinstance(middleware(request), DisallowedHost)


@mock.patch('dalme_app.utils.tenant_context_middleware._tenant')
def test_middleware(mock_ctx, rf, settings):
    """Assert the middleware sets and unsets the context correctly."""
    request = rf.get('/')
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
