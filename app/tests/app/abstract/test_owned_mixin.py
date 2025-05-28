"""Unit tests for owned model and mixin."""

import os
from unittest import mock

import pytest

from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
@mock.patch('app.abstract.owned_mixin.get_current_user')
def test_owner_set_on_create(mock_get_current_user, user, test_model_instance):
    mock_get_current_user.return_value = user
    test_model_instance.save()
    test_model_instance.refresh_from_db()
    assert test_model_instance.owner == user


@pytest.mark.django_db
@mock.patch('app.abstract.owned_mixin.get_current_user')
def test_owner_not_overwritten_on_update(mock_get_current_user, user, test_model):
    mock_get_current_user.return_value = user
    obj = test_model.objects.create(name='test', owner=user)
    obj.name = 'updated'
    obj.save()
    obj.refresh_from_db()
    assert obj.owner == user


@pytest.mark.django_db
@mock.patch('app.abstract.owned_mixin.get_current_user')
def test_owner_not_set_when_data_migration_env(mock_get_current_user, user, test_model_instance):
    mock_get_current_user.return_value = user
    with mock.patch.dict(os.environ, {'DATA_MIGRATION': '1'}):
        test_model_instance.save()
        test_model_instance.refresh_from_db()
        assert test_model_instance.owner is None


@pytest.mark.django_db
def test_save_kwargs_defaults(test_model_instance):
    with mock.patch.object(test_model_instance, 'save', wraps=test_model_instance.save) as mock_save:
        test_model_instance.save()
        _, kwargs = mock_save.call_args
        assert kwargs.get('force_insert', False) is False
        assert kwargs.get('force_update', False) is False
        assert kwargs.get('using', None) is None
        assert kwargs.get('update_fields', None) is None
