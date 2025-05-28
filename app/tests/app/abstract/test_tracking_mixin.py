"""Unit tests for tracking model and mixin."""

import os
from unittest import mock

import pytest

from django.utils import timezone


@pytest.mark.django_db
@mock.patch('app.abstract.tracking_mixin.get_current_user')
@mock.patch('app.abstract.tracking_mixin.timezone')
def test_creation_and_modification_fields_set_on_save(mock_timezone, mock_get_current_user, user, factories):
    now = timezone.now()
    mock_get_current_user.return_value = user
    mock_timezone.now.return_value = now
    obj = factories.tracked_models.create(name='foo')

    assert obj.creation_user == user
    assert obj.modification_user == user
    assert obj.creation_timestamp == now
    assert obj.modification_timestamp == now


@pytest.mark.django_db
@mock.patch('app.abstract.tracking_mixin.get_current_user')
@mock.patch('app.abstract.tracking_mixin.timezone')
def test_modification_fields_update_on_save(mock_timezone, mock_get_current_user, factories):
    user1 = factories.users.create(username='user1')
    user2 = factories.users.create(username='user2')
    time1 = timezone.now()
    time2 = time1 + timezone.timedelta(hours=1)

    mock_get_current_user.return_value = user1
    mock_timezone.now.return_value = time1
    obj = factories.tracked_models.create(name='foo')

    assert obj.creation_user == user1
    assert obj.modification_user == user1
    assert obj.creation_timestamp == time1
    assert obj.modification_timestamp == time1

    mock_get_current_user.return_value = user2
    mock_timezone.now.return_value = time2
    obj.name = 'bar'
    obj.save(is_update=True)

    assert obj.creation_user == user1
    assert obj.modification_user == user2
    assert obj.creation_timestamp == time1
    assert obj.modification_timestamp == time2


@pytest.mark.django_db
@mock.patch.dict(os.environ, {'DATA_MIGRATION': '1'})
@mock.patch('app.abstract.tracking_mixin.get_current_user')
def test_data_migration_env(mock_get_current_user, factories):
    mock_get_current_user.return_value = None  # No user in data migration

    obj = factories.tracked_models.create(name='foo')

    assert obj.creation_user_id == 1
    assert obj.modification_user_id == 1
    assert isinstance(obj.creation_timestamp, timezone.datetime)
    assert isinstance(obj.modification_timestamp, timezone.datetime)


@pytest.mark.django_db
def test_class_name_method(factories):
    obj = factories.tracked_models.create(name='foo')
    assert obj.class_name() == 'TestTracked'
