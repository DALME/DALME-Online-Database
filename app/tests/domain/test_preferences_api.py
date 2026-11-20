"""Test the preferences API and its access policy."""

from unittest import mock

import pytest
from rest_framework import status
from rest_framework.test import force_authenticate

from domain.models import Preference, PreferenceKey


def preferences_view():
    # Importing `domain.api` queries the database (`Agents.queryset` evaluates
    # attribute lists at class definition), so it waits for the db fixture.
    from domain.api.resources.preferences.endpoints import Preferences

    return Preferences


def make_key(name='theme'):
    return PreferenceKey.objects.create(
        name=name,
        label=name,
        description='',
        data_type='STR',
        group='Record Editor',
        default='oneDark',
    )


def list_preferences(arf, user):
    request = arf.get('/api/preferences/')
    force_authenticate(request, user=user)
    return preferences_view().as_view({'get': 'list'})(request)


@pytest.mark.django_db
def test_preferences_list_without_preferences_is_empty(arf, user):
    response = list_preferences(arf, user)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == []


@pytest.mark.django_db
def test_preferences_list_returns_only_the_users_own(arf, user, factories):
    other = factories.users.create(username='other')
    make_key()

    response = list_preferences(arf, user)

    assert response.status_code == status.HTTP_200_OK
    assert [item['id'] for item in response.data] == [Preference.objects.get(user=user).id]
    assert Preference.objects.filter(user=other).exists()


@pytest.mark.django_db
def test_preferences_update_refuses_another_users_preference(arf, user, factories):
    other = factories.users.create(username='other')
    make_key()
    theirs = Preference.objects.get(user=other)
    request = arf.put('/api/preferences/theme/', {'value': 'dracula'}, format='json')
    force_authenticate(request, user=user)

    view = preferences_view()
    with mock.patch.object(view, 'get_object', return_value=theirs):
        response = view.as_view({'put': 'update'})(request, pk='theme')

    assert response.status_code == status.HTTP_403_FORBIDDEN
    theirs.refresh_from_db()
    assert theirs.data == 'oneDark'
