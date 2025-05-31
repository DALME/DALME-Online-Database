"""Tests for TenantMixin functionality."""

import os
from unittest import mock

import pytest

from django.db import models


@pytest.mark.django_db
@mock.patch('tenants.models.tenant_mixin.get_current_tenant')
def test_tenant_field_exists(mock_get_current_tenant, factories, test_tenant):
    mock_get_current_tenant.return_value = test_tenant
    instance = factories.tenanted_models.create(name='TestFieldExists')
    field = instance._meta.model._meta.get_field('tenant')  # noqa: SLF001
    assert isinstance(field, models.ForeignKey)
    assert field.related_model.__name__ == 'Tenant'


@pytest.mark.django_db
@mock.patch('tenants.models.tenant_mixin.get_current_tenant')
def test_is_tenanted_class_attr(mock_get_current_tenant, factories, test_tenant):
    mock_get_current_tenant.return_value = test_tenant
    instance = factories.tenanted_models.create(name='TestIsTenanted')
    assert hasattr(instance._meta.model, 'is_tenanted')  # noqa: SLF001
    assert instance._meta.model.is_tenanted is True  # noqa: SLF001


@pytest.mark.django_db
@mock.patch('tenants.models.tenant_mixin.get_current_tenant')
def test_objects_and_unscoped_managers_exist(mock_get_current_tenant, factories, test_tenant):
    mock_get_current_tenant.return_value = test_tenant
    instance = factories.tenanted_models.create(name='TestObjectsAndUnscoped')
    assert hasattr(instance._meta.model, 'objects')  # noqa: SLF001
    assert hasattr(instance._meta.model, 'unscoped')  # noqa: SLF001


@pytest.mark.django_db
def test_save_does_not_set_tenant_if_data_migration(factories, test_tenant):
    with (
        mock.patch.dict(os.environ, {'DATA_MIGRATION': '1'}),
        mock.patch('tenants.models.tenant_mixin.get_current_tenant') as mock_get_current_tenant,
    ):
        instance = factories.tenanted_models.create(name='TestMigration', tenant=test_tenant)
        instance.save()
        mock_get_current_tenant.assert_not_called()
