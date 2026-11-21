"""Tests for the app.context module."""

import contextvars
from unittest import mock

import pytest
from django_tenants.utils import tenant_context

from django.apps import apps
from django.contrib.contenttypes.models import ContentType

from app import context
from web.extensions.gradients.models import GradientMixin


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


@pytest.mark.django_db
def test_gradient_pages_are_the_page_types_that_carry_a_gradient():
    expected = {
        ContentType.objects.get_for_model(model).id
        for model in apps.get_app_config('web').get_models()
        if issubclass(model, GradientMixin)
    }

    assert expected
    assert set(context.get_gradient_pages()) == expected


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
