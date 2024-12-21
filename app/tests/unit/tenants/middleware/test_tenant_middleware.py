"""Test the app.middleware.tenant_middleware module."""

from unittest import mock

import pytest

from django.core.exceptions import DisallowedHost

from tenants.middleware.tenant_middleware import TenantMiddleware
from tenants.models import Domain, Tenant


@mock.patch('tenants.middleware.tenant_middleware.Domain')
@mock.patch('tenants.middleware.tenant_middleware.connection')
def test_middleware_throws_if_tenant_not_found(mock_conn, mock_domain, rf):
    """Assert the middleware catches non-existant tenants."""
    request = rf.get('/', headers={'HOST': 'some.domain'})
    mock_domain.DoesNotExist = Domain.DoesNotExist
    mock_domain.objects.select_related.return_value.get.side_effect = Domain.DoesNotExist

    get_response = mock.MagicMock()
    middleware = TenantMiddleware(get_response)

    with pytest.raises(DisallowedHost):
        middleware(request)

    assert mock_conn.mock_calls == [
        mock.call.set_schema_to_public(),
    ]


@mock.patch('tenants.middleware.tenant_middleware.Domain')
@mock.patch('tenants.middleware.tenant_middleware.connection')
def test_middleware(mock_conn, mock_domain, rf):
    """Assert the middleware queries and sets the appropriate tenant."""
    request = rf.get('/', headers={'HOST': 'dalme.localhost'})
    mock_domain_obj = mock.MagicMock(spec=Domain)
    mock_tenant = mock.MagicMock(spec=Tenant)
    mock_tenant.get_tenant_type.return_value = 'public'
    mock_domain_obj.tenant = mock_tenant
    mock_domain.objects.select_related.return_value.get.return_value = mock_domain_obj

    get_response = mock.MagicMock()
    middleware = TenantMiddleware(get_response)

    middleware(request)

    assert request.tenant == mock_tenant
    assert mock_conn.mock_calls == [
        mock.call.set_schema_to_public(),
        mock.call.set_tenant(mock_tenant),
    ]
