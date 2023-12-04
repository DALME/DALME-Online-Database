"""Test the ida.middleware.tenant_middleware module."""
from unittest import mock

from django.core.exceptions import DisallowedHost

from ida.middleware.tenant_middleware import TenantMiddleware
from ida.models import Domain, Tenant


@mock.patch('ida.middleware.tenant_middleware.Domain')
@mock.patch('ida.middleware.tenant_middleware.connection')
def test_middleware_throws_if_tenant_not_found(mock_conn, mock_domain, rf):
    """Assert the middleware catches non-existant tenants."""
    request = rf.get('/', headers={'HOST': 'some.domain'})
    mock_domain.DoesNotExist = Domain.DoesNotExist
    mock_domain.objects.select_related.return_value.get.side_effect = Domain.DoesNotExist

    get_response = mock.MagicMock()
    middleware = TenantMiddleware(get_response)

    assert isinstance(middleware(request), DisallowedHost)

    assert mock_conn.mock_calls == [
        mock.call.set_schema_to_public(),
    ]


@mock.patch('ida.middleware.tenant_middleware.Domain')
@mock.patch('ida.middleware.tenant_middleware.connection')
def test_middleware(mock_conn, mock_domain, rf):
    """Assert the middleware queries and sets the appropriate tenant."""
    request = rf.get('/', headers={'HOST': 'dalme.localhost'})
    mock_domain_obj = mock.MagicMock(spec=Domain)
    mock_tenant = mock.MagicMock(spec=Tenant)
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
