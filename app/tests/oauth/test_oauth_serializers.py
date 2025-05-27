"""Test the oauth serializers."""

from unittest import mock

import pytest
from rest_framework.exceptions import ErrorDetail
from rest_framework.serializers import ValidationError

from oauth.serializers import LoginSerializer


@pytest.mark.django_db
def test_login_serializer_no_data():
    data = {}

    serializer = LoginSerializer(data=data)

    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)

    assert serializer.errors == {
        'username': [ErrorDetail(string='This field is required.', code='required')],
        'password': [ErrorDetail(string='This field is required.', code='required')],
    }


@pytest.mark.django_db
def test_login_serializer_missing_credentials(test_email):
    data = {'username': test_email, 'password': ''}

    serializer = LoginSerializer(data=data)

    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)

    assert serializer.errors == {
        'password': [ErrorDetail(string='This field may not be blank.', code='blank')],
    }


@mock.patch('oauth.serializers.authenticate')
@pytest.mark.django_db
def test_login_serializer_incorrect_credentials(mock_authenticate, test_email):
    mock_authenticate.return_value = None
    data = {'username': test_email, 'password': 'incorrect'}

    serializer = LoginSerializer(data=data)

    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)

    assert serializer.errors == {
        'non_field_errors': [
            ErrorDetail(
                string='Access denied: incorrect username or password.',
                code='authorization',
            )
        ],
    }


@mock.patch('oauth.serializers.authenticate')
@pytest.mark.django_db
def test_login_serializer(mock_authenticate, user, test_email, test_password):
    mock_authenticate.return_value = user
    data = {'username': test_email, 'password': test_password}

    serializer = LoginSerializer(data=data)

    assert serializer.is_valid(raise_exception=True)
    # This serializer is just for managing the authenticate side-effect so we
    # don't expect it to render anything out to a representation.
    assert serializer.data == {}
