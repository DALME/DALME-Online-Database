"""Tests for the app.context module."""

import contextvars
from unittest import mock

import pytest
from django_tenants.utils import tenant_context

from app import context


@pytest.mark.django_db
def test_bibliography_choices_follow_the_project_on_one_thread(factories, test_tenant, other_tenant):
    with tenant_context(test_tenant):
        ours = factories.bibliography_pages.create()
    with tenant_context(other_tenant):
        theirs = factories.bibliography_pages.create()

    def choices_in(tenant):
        with tenant_context(tenant):
            return context.get_biblio_pages()

    # One context stands for one worker thread serving both projects in turn.
    first, second = contextvars.copy_context().run(lambda: (choices_in(test_tenant), choices_in(other_tenant)))

    assert first == [(ours.pk, ours.short_title)]
    assert second == [(theirs.pk, theirs.short_title)]


def test_get_gradient_pages_sets_and_returns_ids():
    mock_app_config = mock.Mock()
    mock_model = mock.Mock()
    mock_model.__name__ = 'TestModel'
    mock_field = mock.Mock()
    mock_field.name = 'gradient'
    mock_model._meta.get_fields.return_value = [mock_field]  # noqa: SLF001
    mock_app_config.models_module = True
    mock_app_config.get_models.return_value = [mock_model]

    with (
        mock.patch('app.context.apps.get_app_config', return_value=mock_app_config),
        mock.patch('app.context.ContentType.objects.filter') as mock_filter,
    ):
        mock_ct = mock.Mock()
        mock_ct.id = 42
        mock_filter.return_value = [mock_ct]
        result = context.get_gradient_pages()
        assert result == [42]
        # Should return cached value on second call
        assert context.get_gradient_pages() == [42]


def test_get_gradient_pages_returns_cached_value():
    context._gradient_pages.set([1, 2, 3])  # noqa: SLF001
    assert context.get_gradient_pages() == [1, 2, 3]


@pytest.mark.django_db
def test_a_bibliography_without_a_short_title_is_listed_by_its_title(factories, test_tenant):
    with tenant_context(test_tenant):
        page = factories.bibliography_pages.create(short_title='')

        assert context.get_biblio_pages() == [(page.pk, page.title)]


def test_get_current_username_returns_username(test_username):
    mock_user = mock.Mock()
    mock_user.username = test_username
    with mock.patch('app.context.get_current_user', return_value=mock_user):
        assert context.get_current_username() == test_username
