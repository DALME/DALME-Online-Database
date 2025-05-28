"""Test the app.middleware.tenant_middleware module."""

from unittest import mock

import pytest

from django.core.exceptions import DisallowedHost

from tenants.middleware.tenant_middleware import TenantMiddleware
from tenants.models import Domain


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


@mock.patch('tenants.middleware.tenant_middleware.connection')
@pytest.mark.django_db
def test_middleware(mock_conn, test_domain, rf):
    """Assert the middleware queries and sets the appropriate tenant."""
    request = rf.get('/', headers={'HOST': test_domain.domain})
    get_response = mock.MagicMock()
    middleware = TenantMiddleware(get_response)
    middleware(request)

    assert request.tenant == test_domain.tenant
    assert mock_conn.mock_calls == [
        mock.call.set_schema_to_public(),
        mock.call.set_tenant(test_domain.tenant),
    ]
