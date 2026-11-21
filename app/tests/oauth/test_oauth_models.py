"""Test the oauth models."""

import pytest

from django.contrib.auth.models import Group

from oauth.models import GroupProperties, User

from tests.factories.fakers import fake


@pytest.mark.django_db
def test_a_group_keeps_the_tenant_it_was_created_under(as_tenant, test_tenant, other_tenant):
    with as_tenant(test_tenant):
        group = Group.objects.create(name=fake.word())
        properties = GroupProperties.objects.create(
            group=group,
            group_type=GroupProperties.TEAM,
            description=fake.sentence(),
        )

    with as_tenant(other_tenant):
        assert properties.tenant.pk == test_tenant.pk


def test_user_creation_error():
    with pytest.raises(ValueError) as exc:  # noqa: PT011
        User.objects.create_user(username=None)

    assert str(exc.value) == 'The given username must be set'


def test_superuser_creation_error_is_staff(test_username, test_password):
    with pytest.raises(ValueError) as exc:  # noqa: PT011
        User.objects.create_superuser(
            username=test_username,
            password=test_password,
            is_staff=False,
        )

    assert str(exc.value) == 'Superuser must have is_staff=True.'


def test_superuser_creation_error_is_superuser(test_username, test_password):
    with pytest.raises(ValueError) as exc:  # noqa: PT011
        User.objects.create_superuser(
            username=test_username,
            password=test_password,
            is_superuser=False,
        )

    assert str(exc.value) == 'Superuser must have is_superuser=True.'


@pytest.mark.django_db
def test_user_creation(test_username):
    user = User.objects.create_user(username=test_username)
    assert isinstance(user.pk, int)


@pytest.mark.django_db
def test_superuser_creation(test_username, test_password):
    user = User.objects.create_superuser(username=test_username, password=test_password)
    assert isinstance(user.pk, int)


@pytest.mark.django_db
def test_user_creation_bulk(test_username, factories):
    objs = [User(username=test_username), User(username=factories.users.build().username)]
    users = User.objects.bulk_create(objs)

    assert all(isinstance(user.pk, int) for user in users)
