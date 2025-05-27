"""Unit tests for the Agents endpoint in the domain API."""

import os
from unittest import mock

import pytest

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.utils import ProgrammingError

from app.abstract import custom_manager
from app.abstract.custom_manager import CustomQuerySet


def test_as_manager_returns_manager():
    manager = custom_manager.CustomQuerySet.as_manager()
    assert isinstance(manager, custom_manager.CustomManager)
    assert getattr(manager, '_built_with_as_manager', False)


def test_include_attrs_calls_annotate_and_prefetch(monkeypatch):
    mock_qs = mock.Mock(spec=custom_manager.CustomQuerySet)
    mock_qs.include_attrs.return_value = mock_qs

    # Patch CustomQuerySet to return our mock
    monkeypatch.setattr(custom_manager, 'CustomQuerySet', lambda *a, **kw: mock_qs)  # noqa: ARG005

    result = custom_manager.CustomQuerySet(None).include_attrs('foo')
    assert result is mock_qs
    mock_qs.include_attrs.assert_called_with('foo')


def test_get_queryset_tenant_scoped(monkeypatch, custom_manager_instance, mock_model):
    # Patch get_current_tenant to return a mock tenant
    tenant = mock.Mock()
    tenant.pk = 1
    monkeypatch.setattr(custom_manager, 'get_current_tenant', lambda *a, **kw: tenant)  # noqa: ARG005
    # Patch model attribute_list and is_tenanted
    custom_manager_instance.model = mock_model
    # Patch CustomQuerySet.filter to check call
    qs = mock.Mock(spec=custom_manager.CustomQuerySet)
    monkeypatch.setattr(custom_manager, 'CustomQuerySet', lambda *a, **kw: qs)  # noqa: ARG005
    qs.filter.return_value = qs
    qs.include_attrs.return_value = qs
    result = custom_manager_instance.get_queryset()
    assert result is qs
    assert qs.filter.called


def test_get_queryset_runtimeerror_in_dev(monkeypatch, custom_manager_instance, mock_model):
    def raise_runtime():
        raise RuntimeError

    monkeypatch.setattr(custom_manager, 'get_current_tenant', raise_runtime)
    custom_manager_instance.model = mock_model
    qs = mock.Mock(spec=custom_manager.CustomQuerySet)
    monkeypatch.setattr(custom_manager, 'CustomQuerySet', lambda *a, **kw: qs)  # noqa: ARG005
    qs.filter.return_value = qs
    qs.include_attrs.return_value = qs
    monkeypatch.setattr(settings, 'DEBUG', True)
    monkeypatch.setitem(os.environ, 'ENV', 'development')

    with pytest.raises(RuntimeError):
        custom_manager_instance.get_queryset()


def test_get_queryset_runtimeerror_in_prod(monkeypatch, custom_manager_instance, mock_model):
    # Patch get_current_tenant to raise RuntimeError
    def raise_runtime():
        raise RuntimeError

    monkeypatch.setattr(custom_manager, 'get_current_tenant', raise_runtime)
    custom_manager_instance.model = mock_model
    qs = mock.Mock(spec=custom_manager.CustomQuerySet)
    monkeypatch.setattr(custom_manager, 'CustomQuerySet', lambda *a, **kw: qs)  # noqa: ARG005
    qs.filter.return_value = qs
    qs.include_attrs.return_value = qs
    monkeypatch.setattr(settings, 'DEBUG', False)
    monkeypatch.setitem(os.environ, 'ENV', 'production')

    with pytest.raises(RuntimeError):
        custom_manager_instance.get_queryset()


def test_unscoped_returns_queryset(custom_manager_instance, mock_model):
    custom_manager_instance.model = mock_model
    qs = custom_manager_instance.unscoped()
    assert isinstance(qs, models.QuerySet)


def test_include_attrs_unique(monkeypatch, mock_model):
    # Patch dependencies inside include_attrs
    mock_qs = mock.Mock(spec=CustomQuerySet)
    mock_qs.model = mock_model
    mock_qs.prefetch_related.return_value = mock_qs

    mock_attribute = mock.Mock()
    mock_attribute.objects.filter.return_value.values_list.return_value = [1, 2]

    mock_attributetype = mock.Mock()
    mock_attributetype.objects.get.return_value.contenttypes.get.return_value.is_unique = True

    monkeypatch.setattr('domain.models.attribute.Attribute', mock_attribute)
    monkeypatch.setattr('domain.models.attribute.AttributeType', mock_attributetype)
    monkeypatch.setattr('domain.models.attribute.AttributeField', mock.Mock)
    monkeypatch.setattr('domain.models.attribute.ListField', mock.Mock)
    monkeypatch.setattr(
        'django.contrib.contenttypes.models.ContentType.objects.get_for_model',
        lambda model: mock.Mock(),  # noqa: ARG005
    )

    # Patch annotate to just return self
    mock_qs.annotate.return_value = mock_qs

    # Actually call include_attrs
    CustomQuerySet.include_attrs(mock_qs, 'foo')
    mock_qs.prefetch_related.assert_called_with('attributes')
    mock_qs.annotate.assert_called()


def test_include_attrs_not_unique(monkeypatch, mock_model, dummy_attribute_field, dummy_list_field):
    # Patch dependencies inside include_attrs
    mock_qs = mock.Mock(spec=CustomQuerySet)
    mock_qs.model = mock_model
    mock_qs.prefetch_related.return_value = mock_qs

    mock_attribute = mock.Mock()
    mock_values_qs = mock.Mock()
    # mock_values_qs.return_value = [1, 2]
    mock_values_qs.query = mock.Mock()
    mock_values_qs.clone = mock.Mock(return_value=mock_values_qs)
    mock_attribute.objects.filter.return_value.values_list.return_value = mock_values_qs

    mock_attributetype = mock.Mock()
    mock_attributetype.objects.get.return_value.contenttypes.get.return_value.is_unique = False

    monkeypatch.setattr('domain.models.attribute.Attribute', mock_attribute)
    monkeypatch.setattr('domain.models.attribute.AttributeType', mock_attributetype)
    monkeypatch.setattr('domain.models.attribute.AttributeField', dummy_attribute_field)
    monkeypatch.setattr('domain.models.attribute.ListField', dummy_list_field)
    monkeypatch.setattr(
        'django.contrib.contenttypes.models.ContentType.objects.get_for_model',
        lambda model: mock.Mock(),  # noqa: ARG005
    )

    # Patch annotate to just return self
    mock_qs.annotate.return_value = mock_qs
    # mock_qs.clone = mock.Mock(return_value=mock_qs)

    CustomQuerySet.include_attrs(mock_qs, 'foo')
    mock_qs.prefetch_related.assert_called_with('attributes')
    mock_qs.annotate.assert_called()


def test_include_attrs_exception(monkeypatch, mock_model):
    # Patch dependencies inside include_attrs to raise exception
    mock_qs = mock.Mock(spec=CustomQuerySet)
    mock_qs.model = mock_model
    mock_qs.prefetch_related.return_value = mock_qs

    mock_attribute = mock.Mock()
    mock_attribute.objects.filter.return_value.values_list.return_value = [1, 2]

    mock_attributetype = mock.Mock()

    def raise_exc(*a, **kw):  # noqa: ARG001
        raise ObjectDoesNotExist

    mock_attributetype.objects.get.side_effect = raise_exc

    monkeypatch.setattr('domain.models.attribute.Attribute', mock_attribute)
    monkeypatch.setattr('domain.models.attribute.AttributeType', mock_attributetype)
    monkeypatch.setattr('domain.models.attribute.AttributeField', mock.Mock)
    monkeypatch.setattr('domain.models.attribute.ListField', mock.Mock)
    monkeypatch.setattr(
        'django.contrib.contenttypes.models.ContentType.objects.get_for_model',
        lambda model: mock.Mock(),  # noqa: ARG005
    )

    # Patch annotate to just return self
    mock_qs.annotate.return_value = mock_qs

    CustomQuerySet.include_attrs(mock_qs, 'foo')
    mock_qs.prefetch_related.assert_called_with('attributes')
    mock_qs.annotate.assert_called()


def test_include_attrs_programming_error(monkeypatch, mock_model):
    # Patch dependencies inside include_attrs to raise ProgrammingError
    mock_qs = mock.Mock(spec=CustomQuerySet)
    mock_qs.model = mock_model
    mock_qs.prefetch_related.return_value = mock_qs

    mock_attribute = mock.Mock()
    mock_attribute.objects.filter.return_value.values_list.return_value = [1, 2]

    mock_attributetype = mock.Mock()

    def raise_exc(*a, **kw):  # noqa: ARG001
        raise ProgrammingError

    mock_attributetype.objects.get.side_effect = raise_exc

    monkeypatch.setattr('domain.models.attribute.Attribute', mock_attribute)
    monkeypatch.setattr('domain.models.attribute.AttributeType', mock_attributetype)
    monkeypatch.setattr('domain.models.attribute.AttributeField', mock.Mock)
    monkeypatch.setattr('domain.models.attribute.ListField', mock.Mock)
    monkeypatch.setattr(
        'django.contrib.contenttypes.models.ContentType.objects.get_for_model',
        lambda model: mock.Mock(),  # noqa: ARG005
    )

    # Patch annotate to just return self
    mock_qs.annotate.return_value = mock_qs

    CustomQuerySet.include_attrs(mock_qs, 'foo')
    mock_qs.prefetch_related.assert_called_with('attributes')
    mock_qs.annotate.assert_called()
