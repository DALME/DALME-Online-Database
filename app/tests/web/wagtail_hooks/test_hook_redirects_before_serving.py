"""Tests for hook redirects_before_serving."""

from unittest import mock

import pytest

from web.wagtail_hooks.redirects_before_serving import add_redirects_before_serving_pages


@pytest.mark.urls('app.urls.urls_tenant')
@pytest.mark.django_db
@mock.patch('app.abstract.custom_manager.get_current_tenant')
@mock.patch('web.wagtail_hooks.redirects_before_serving.redirect')
def test_redirects_root_page(mock_redirect, mock_get_current_tenant, test_site, test_tenant, rf):
    mock_get_current_tenant.return_value = test_tenant
    home_page = test_site.root_page
    assert home_page.is_root()
    request = rf.get('/', headers={'HOST': test_site.hostname})
    result = add_redirects_before_serving_pages(home_page, request, None, None)
    mock_redirect.assert_called_once_with(home_page.get_children().live().first().get_url(request), permanent=False)
    assert result == mock_redirect.return_value


@pytest.mark.urls('app.urls.urls_tenant')
@pytest.mark.django_db
@mock.patch('app.abstract.custom_manager.get_current_tenant')
@mock.patch('web.wagtail_hooks.redirects_before_serving.redirect')
def test_redirects_section_with_child(mock_redirect, mock_get_current_tenant, test_site, test_tenant, rf):
    mock_get_current_tenant.return_value = test_tenant
    home_page = test_site.root_page
    section = home_page.get_children().filter(title='Section 1').first().specific
    assert section._meta.label == 'web.Section'  # noqa: SLF001
    request = rf.get(f'{section.get_full_url()}', headers={'HOST': test_site.hostname})
    child_slug = section.get_children().live().first().slug
    result = add_redirects_before_serving_pages(section, request, None, None)
    mock_redirect.assert_called_once_with(f'/{section.slug}/{child_slug}/', permanent=False)
    assert result == mock_redirect.return_value


@pytest.mark.urls('app.urls.urls_tenant')
@pytest.mark.django_db
@mock.patch('app.abstract.custom_manager.get_current_tenant')
@mock.patch('web.wagtail_hooks.redirects_before_serving.redirect')
def test_redirects_section_without_child(mock_redirect, mock_get_current_tenant, factories, test_site, test_tenant, rf):
    mock_get_current_tenant.return_value = test_tenant
    home_page = test_site.root_page
    section = factories.pages_sections.create(parent=home_page, slug='section')
    assert section._meta.label == 'web.Section'  # noqa: SLF001
    assert section.get_children().live().first() is None
    assert section.get_ancestors().last().slug == 'home-page'
    request = rf.get(f'{section.get_full_url()}', headers={'HOST': test_site.hostname})
    result = add_redirects_before_serving_pages(section, request, None, None)
    mock_redirect.assert_called_once_with(home_page.get_children().live().first().get_url(request), permanent=False)
    assert result == mock_redirect.return_value


@pytest.mark.urls('app.urls.urls_tenant')
@pytest.mark.django_db
@mock.patch('app.abstract.custom_manager.get_current_tenant')
def test_no_redirect_for_other_pages(mock_get_current_tenant, test_site, factories, test_tenant, rf):
    mock_get_current_tenant.return_value = test_tenant
    home_page = test_site.root_page
    page = factories.flat_pages.create(parent=home_page, slug='some-page')
    request = rf.get(f'{page.get_full_url()}', headers={'HOST': test_site.hostname})
    result = add_redirects_before_serving_pages(page, request, None, None)
    assert result is None
