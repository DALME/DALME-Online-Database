"""Test the oauth models."""

import pytest

from oauth.models import User


def test_user_creation_error():
    with pytest.raises(ValueError) as exc:  # noqa: PT011
        User.objects.create_user(username=None)

    assert str(exc.value) == 'The given username must be set'


def test_superuser_creation_error_is_staff(test_username):
    with pytest.raises(ValueError) as exc:  # noqa: PT011
        User.objects.create_superuser(
            username=test_username,
            password='password123',
            is_staff=False,
        )

    assert str(exc.value) == 'Superuser must have is_staff=True.'


def test_superuser_creation_error_is_superuser(test_username):
    with pytest.raises(ValueError) as exc:  # noqa: PT011
        User.objects.create_superuser(
            username=test_username,
            password='password123',
            is_superuser=False,
        )

    assert str(exc.value) == 'Superuser must have is_superuser=True.'


@pytest.mark.django_db
def test_user_creation(test_username):
    user = User.objects.create_user(username=test_username)
    assert isinstance(user.pk, int)


@pytest.mark.django_db
def test_superuser_creation(test_username):
    user = User.objects.create_superuser(username=test_username, password='password123')
    assert isinstance(user.pk, int)


@pytest.mark.django_db
def test_user_creation_bulk(test_username):
    objs = [User(username=test_username), User(username='another.username')]
    users = User.objects.bulk_create(objs)

    assert all(isinstance(user.pk, int) for user in users)
