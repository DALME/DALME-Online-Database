"""Test the app.middleware.tenant_context_middleware module."""

from unittest import mock

import pytest
from werkzeug.local import LocalProxy

from django.core.exceptions import DisallowedHost
from django.http import HttpResponse

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


@pytest.mark.django_db
@pytest.mark.usefixtures('settings')
def test_the_view_runs_with_the_tenant_bound_and_releases_it(rf, test_domain):
    seen = []

    def view(request):  # noqa: ARG001
        seen.append(get_current_tenant()._get_current_object())  # noqa: SLF001
        return HttpResponse()

    request = rf.get('/', headers={'HOST': test_domain.domain})
    request.tenant = test_domain.tenant

    TenantContextMiddleware(view)(request)

    assert seen == [test_domain.tenant]
    assert not get_current_tenant()


@pytest.mark.django_db
@pytest.mark.usefixtures('settings')
def test_a_failing_view_releases_the_tenant(rf, test_domain):
    request = rf.get('/', headers={'HOST': test_domain.domain})
    request.tenant = test_domain.tenant
    middleware = TenantContextMiddleware(mock.Mock(side_effect=ValueError))

    with pytest.raises(ValueError):  # noqa: PT011
        middleware(request)

    assert not get_current_tenant()


@pytest.mark.django_db
def test_middleware_writes_neither_the_site_name_nor_a_public_url(rf, settings, test_domain):
    site_name = settings.WAGTAIL_SITE_NAME
    request = rf.get('/', headers={'HOST': test_domain.domain})
    request.tenant = test_domain.tenant

    TenantContextMiddleware(mock.MagicMock())(request)

    assert settings.WAGTAIL_SITE_NAME is site_name
    assert not hasattr(settings, 'PUBLIC_URL')


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
    assert isinstance(set_tenant, LocalProxy)
    assert mock_ctx.mock_calls == [
        mock.call.set(tenant),
        mock.call.reset(mock_ctx.set.return_value),
    ]
