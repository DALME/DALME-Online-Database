"""Tests for the non-tenant-specific URL patterns in the app."""

from unittest import mock

import pytest

from django.urls import resolve


@pytest.mark.parametrize(
    ('path', 'namespace', 'view_name'),
    [
        ('/admin/', None, 'admin:index'),
        ('/api/', 'api', None),
    ],
)
@pytest.mark.urls('app.urls.urls')
@pytest.mark.django_db
@mock.patch('app.abstract.custom_manager.get_current_tenant')
def test_urlpatterns_resolve_known_paths(mock_get_current_tenant, path, namespace, view_name, test_domain):
    mock_get_current_tenant.return_value = test_domain.tenant
    # This will raise Resolver404 if not found
    resolver = resolve(path)
    if namespace:
        assert resolver.namespace == namespace
    if view_name:
        assert resolver.view_name == view_name


@pytest.mark.urls('app.urls.urls')
@pytest.mark.django_db
@mock.patch('app.abstract.custom_manager.get_current_tenant')
def test_home_url_resolves(mock_get_current_tenant, test_domain):
    mock_get_current_tenant.return_value = test_domain.tenant
    resolver = resolve('/')
    assert resolver.func.view_class.__name__ == 'TemplateView'


@pytest.mark.urls('app.urls.urls_tenant')
@pytest.mark.django_db
@mock.patch('app.abstract.custom_manager.get_current_tenant')
def test_web_urls_included(mock_get_current_tenant, test_domain):
    mock_get_current_tenant.return_value = test_domain.tenant
    # web_urls are included via unpacking
    # Just check that at least one of their patterns is present in urlpatterns
    from app.urls import urls_tenant
    from web.urls import urlpatterns as web_urls

    found = False
    for web_url in web_urls:
        for url in urls_tenant.urlpatterns:
            if getattr(web_url, 'pattern', None) == getattr(url, 'pattern', None):
                found = True
                break
    assert found, 'web_urls not included in urlpatterns'


@pytest.mark.urls('app.urls.urls_tenant')
@pytest.mark.django_db
@mock.patch('app.abstract.custom_manager.get_current_tenant')
def test_wagtail_serve_pattern(mock_get_current_tenant, test_domain):
    mock_get_current_tenant.return_value = test_domain.tenant
    from app.urls import urls_tenant

    # The last re_path should be wagtail's catch-all
    pattern = urls_tenant.urlpatterns[-1]  # staticfiles_urlpatterns() is appended last
    assert pattern.name == 'wagtail_serve'
    assert pattern.pattern.regex.pattern == r'^((?:[\w\-:]+/)*)$'
