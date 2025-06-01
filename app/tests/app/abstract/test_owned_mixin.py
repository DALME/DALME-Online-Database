"""Unit tests for owned model and mixin."""

import os
from unittest import mock

import pytest


@pytest.mark.django_db
@mock.patch('app.abstract.owned_mixin.get_current_user')
def test_owner_set_on_create(mock_get_current_user, user, factories):
    mock_get_current_user.return_value = user
    obj = factories.owned_models.create(name='test_create')
    assert obj.owner == user


@pytest.mark.django_db
@mock.patch('app.abstract.owned_mixin.get_current_user')
def test_owner_not_overwritten_on_update(mock_get_current_user, factories):
    user1 = factories.users.create(username='user1')
    user2 = factories.users.create(username='user2')
    mock_get_current_user.return_value = user1
    obj = factories.owned_models.create(name='test_update')
    mock_get_current_user.return_value = user2
    obj.name = 'updated'
    assert obj.owner == user1


@pytest.mark.django_db
@mock.patch.dict(os.environ, {'DATA_MIGRATION': '1'})
@mock.patch('app.abstract.owned_mixin.get_current_user')
def test_owner_not_set_when_data_migration_env(mock_get_current_user, user, factories):
    mock_get_current_user.return_value = user
    obj = factories.owned_models.create(name='test_migration')
    assert obj.owner is None


@pytest.mark.django_db
def test_save_kwargs_defaults(factories):
    obj = factories.owned_models
    with mock.patch.object(obj, '_create', wraps=obj._create) as mock_save:  # noqa: SLF001
        obj.create(name='test_save_kwargs')
        _, kwargs = mock_save.call_args
        assert kwargs.get('force_insert', False) is False
        assert kwargs.get('force_update', False) is False
        assert kwargs.get('using', None) is None
        assert kwargs.get('update_fields', None) is None


@pytest.mark.django_db
def test_class_name_returns_class_name(factories):
    obj = factories.owned_models.create(name='test_update')
    assert obj.class_name() == 'TestOwned'
