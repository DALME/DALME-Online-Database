"""Test the preferences API and its access policy."""

from unittest import mock

import pytest
from rest_framework import status
from rest_framework.test import force_authenticate

from domain.models import Preference


def list_preferences(view, arf, user):
    request = arf.get('/api/preferences/')
    force_authenticate(request, user=user)
    return view.as_view({'get': 'list'})(request)


@pytest.mark.django_db
def test_preferences_list_without_preferences_is_empty(preferences_view, arf, user):
    response = list_preferences(preferences_view, arf, user)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == []


@pytest.mark.django_db
def test_preferences_list_returns_only_the_users_own(preferences_view, preference_key, arf, user, factories):
    other = factories.users.create(username='other')
    Preference.objects.filter(user=other, key=preference_key).update(data='dracula')

    response = list_preferences(preferences_view, arf, user)

    assert response.status_code == status.HTTP_200_OK
    assert [(item['name'], item['value']) for item in response.data] == [('theme', 'oneDark')]


@pytest.mark.django_db
def test_preferences_update_refuses_another_users_preference(preferences_view, preference_key, arf, user, factories):
    other = factories.users.create(username='other')
    theirs = Preference.objects.get(user=other, key=preference_key)
    request = arf.put('/api/preferences/theme/', {'value': 'dracula'}, format='json')
    force_authenticate(request, user=user)

    with mock.patch.object(preferences_view, 'get_object', return_value=theirs):
        response = preferences_view.as_view({'put': 'update'})(request, pk='theme')

    assert response.status_code == status.HTTP_403_FORBIDDEN
    theirs.refresh_from_db()
    assert theirs.data == 'oneDark'
