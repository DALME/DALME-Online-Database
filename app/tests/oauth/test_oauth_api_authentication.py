"""Test the oauth authentication API."""

import pytest
from freezegun import freeze_time
from rest_framework import status
from rest_framework.exceptions import ErrorDetail

from django.contrib.sessions.backends.db import SessionStore
from django.urls import reverse

from oauth.api.authentication import AuthorizationCode, Login


@pytest.mark.urls('app.urls.urls_tenant')
def test_oauth_authorization_code_no_credentials(arf, log, set_mock_tenant):  # noqa: ARG001
    view = AuthorizationCode.as_view()

    url = reverse('oauth:authorization-code')
    request = arf.get(url, format='json')
    response = view(request)

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.data == {
        'detail': ErrorDetail(
            string='Authentication credentials were not provided.',
            code='not_authenticated',
        ),
    }
    assert not log.events


@freeze_time('1970-01-01')
@pytest.mark.urls('app.urls.urls_tenant')
@pytest.mark.django_db
def test_oauth_login_missing_credentials(arf, test_username, user, log, set_mock_tenant):  # noqa: ARG001
    view = Login.as_view()
    session = SessionStore()

    assert user.last_login is None

    url = reverse('oauth:login')
    request = arf.post(
        url,
        {
            'username': test_username,
        },
        format='json',
    )
    request.session = session
    response = view(request)

    user.refresh_from_db()

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {
        'password': [
            ErrorDetail(
                string='This field is required.',
                code='required',
            ),
        ],
    }
    assert user.last_login is None
    assert not log.events


@freeze_time('1970-01-01')
@pytest.mark.urls('app.urls.urls_tenant')
@pytest.mark.django_db
def test_oauth_login_incorrect_credentials(arf, test_username, user, log, set_mock_tenant):  # noqa: ARG001
    view = Login.as_view()
    session = SessionStore()

    assert user.last_login is None

    url = reverse('oauth:login')
    request = arf.post(
        url,
        {
            'username': test_username,
            'password': 'incorrect123',
        },
        format='json',
    )
    request.session = session
    response = view(request)

    user.refresh_from_db()

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {
        'non_field_errors': [
            ErrorDetail(
                string='Access denied: incorrect username or password.',
                code='authorization',
            ),
        ]
    }
    assert user.last_login is None
    assert not log.events


@freeze_time('1970-01-01')
@pytest.mark.urls('app.urls.urls_tenant')
@pytest.mark.django_db
def test_oauth_login(arf, test_username, test_password, user, unix_epoch_datetime, log, set_mock_tenant):  # noqa: ARG001
    view = Login.as_view()
    session = SessionStore()

    assert user.last_login is None

    url = reverse('oauth:login')
    request = arf.post(
        url,
        {
            'username': test_username,
            'password': test_password,
        },
        format='json',
    )
    request.session = session
    response = view(request)

    user.refresh_from_db()
    assert response.status_code == status.HTTP_202_ACCEPTED
    assert response.data is None
    assert session['_auth_user_id'] == str(user.pk)
    assert user.last_login == unix_epoch_datetime
    assert log.events == [
        {'event': 'User successfully logged in', 'level': 'info', 'user': user},
    ]
