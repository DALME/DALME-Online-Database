"""Unit tests for the custom model manager."""

import os
from unittest import mock

import pytest

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import ProgrammingError

from app.abstract import custom_manager
from app.abstract.custom_manager import CustomQuerySet


def test_as_manager_returns_manager():
    manager = custom_manager.CustomQuerySet.as_manager()
    assert isinstance(manager, custom_manager.CustomManager)
    assert getattr(manager, '_built_with_as_manager', False)


def test_include_attrs_calls_annotate_and_prefetch():
    mock_qs = mock.Mock(spec=custom_manager.CustomQuerySet)
    mock_qs.include_attrs.return_value = mock_qs

    # Patch CustomQuerySet to return our mock
    with mock.patch.object(custom_manager, 'CustomQuerySet', return_value=mock_qs):
        result = custom_manager.CustomQuerySet(None).include_attrs('foo')
        assert result is mock_qs
        mock_qs.include_attrs.assert_called_with('foo')


def test_get_queryset_tenant_scoped(custom_manager_instance, test_model):
    tenant = mock.Mock()
    tenant.pk = 1
    with mock.patch.object(custom_manager, 'get_current_tenant', return_value=tenant):
        custom_manager_instance.model = test_model
        qs = mock.Mock(spec=custom_manager.CustomQuerySet)
        with mock.patch.object(custom_manager, 'CustomQuerySet', return_value=qs):
            qs.filter.return_value = qs
            qs.include_attrs.return_value = qs
            result = custom_manager_instance.get_queryset()
            assert result is qs
            assert qs.filter.called


def test_get_queryset_runtimeerror_in_dev(custom_manager_instance, test_model):
    def raise_runtime():
        raise RuntimeError

    with mock.patch.object(custom_manager, 'get_current_tenant', raise_runtime):
        custom_manager_instance.model = test_model
        qs = mock.Mock(spec=custom_manager.CustomQuerySet)
        with mock.patch.object(custom_manager, 'CustomQuerySet', return_value=qs):
            qs.filter.return_value = qs
            qs.include_attrs.return_value = qs
            with (
                mock.patch.object(settings, 'DEBUG', True),
                mock.patch.dict(os.environ, {'ENV': 'development'}),
                pytest.raises(RuntimeError),
            ):
                custom_manager_instance.get_queryset()


def test_get_queryset_runtimeerror_in_prod(custom_manager_instance, test_model):
    def raise_runtime():
        raise RuntimeError

    with mock.patch.object(custom_manager, 'get_current_tenant', raise_runtime):
        custom_manager_instance.model = test_model
        qs = mock.Mock(spec=custom_manager.CustomQuerySet)
        with mock.patch.object(custom_manager, 'CustomQuerySet', return_value=qs):
            qs.filter.return_value = qs
            qs.include_attrs.return_value = qs
            with (
                mock.patch.object(settings, 'DEBUG', False),
                mock.patch.dict(os.environ, {'ENV': 'production'}),
                pytest.raises(RuntimeError),
            ):
                custom_manager_instance.get_queryset()


def test_get_queryset_runtimeerror_returns_unfiltered(custom_manager_instance, test_model):
    custom_manager_instance.model = test_model
    qs = mock.Mock(spec=custom_manager.CustomQuerySet)
    with mock.patch.object(custom_manager, 'CustomQuerySet', return_value=qs):
        qs.filter.return_value = qs
        qs.include_attrs.return_value = qs
        with (
            mock.patch.object(settings, 'DEBUG', True),
            mock.patch.dict(os.environ, {'ENV': 'development'}),
        ):
            assert qs == custom_manager_instance.get_queryset()


def test_include_attrs_unique(test_model):
    mock_qs = mock.Mock(spec=CustomQuerySet)
    mock_qs.model = test_model
    mock_qs.prefetch_related.return_value = mock_qs

    mock_attribute = mock.Mock()
    mock_attribute.objects.filter.return_value.values_list.return_value = [1, 2]

    mock_attributetype = mock.Mock()
    mock_attributetype.objects.get.return_value.contenttypes.get.return_value.is_unique = True

    with (
        mock.patch('domain.models.attribute.Attribute', mock_attribute),
        mock.patch('domain.models.attribute.AttributeType', mock_attributetype),
        mock.patch('domain.models.attribute.AttributeField', mock.Mock),
        mock.patch('domain.models.attribute.ListField', mock.Mock),
        mock.patch('django.contrib.contenttypes.models.ContentType.objects.get_for_model', return_value=mock.Mock()),
    ):
        mock_qs.annotate.return_value = mock_qs
        CustomQuerySet.include_attrs(mock_qs, 'foo')
        mock_qs.prefetch_related.assert_called_with('attributes')
        mock_qs.annotate.assert_called()


def test_include_attrs_not_unique(test_model):
    class DummyAttributeField:
        pass

    class DummyListField:
        def __init__(self, *a, **kw):
            pass

    mock_qs = mock.Mock(spec=CustomQuerySet)
    mock_qs.model = test_model
    mock_qs.prefetch_related.return_value = mock_qs

    mock_attribute = mock.Mock()
    mock_values_qs = mock.Mock()
    mock_values_qs.query = mock.Mock()
    mock_values_qs.clone = mock.Mock(return_value=mock_values_qs)
    mock_attribute.objects.filter.return_value.values_list.return_value = mock_values_qs

    mock_attributetype = mock.Mock()
    mock_attributetype.objects.get.return_value.contenttypes.get.return_value.is_unique = False

    with (
        mock.patch('domain.models.attribute.Attribute', mock_attribute),
        mock.patch('domain.models.attribute.AttributeType', mock_attributetype),
        mock.patch('domain.models.attribute.AttributeField', DummyAttributeField),
        mock.patch('domain.models.attribute.ListField', DummyListField),
        mock.patch('django.contrib.contenttypes.models.ContentType.objects.get_for_model', return_value=mock.Mock()),
    ):
        mock_qs.annotate.return_value = mock_qs
        CustomQuerySet.include_attrs(mock_qs, 'foo')
        mock_qs.prefetch_related.assert_called_with('attributes')
        mock_qs.annotate.assert_called()


def test_include_attrs_exception(test_model):
    mock_qs = mock.Mock(spec=CustomQuerySet)
    mock_qs.model = test_model
    mock_qs.prefetch_related.return_value = mock_qs

    mock_attribute = mock.Mock()
    mock_attribute.objects.filter.return_value.values_list.return_value = [1, 2]

    mock_attributetype = mock.Mock()

    def raise_exc(*a, **kw):  # noqa: ARG001
        raise ObjectDoesNotExist

    mock_attributetype.objects.get.side_effect = raise_exc

    with (
        mock.patch('domain.models.attribute.Attribute', mock_attribute),
        mock.patch('domain.models.attribute.AttributeType', mock_attributetype),
        mock.patch('domain.models.attribute.AttributeField', mock.Mock),
        mock.patch('domain.models.attribute.ListField', mock.Mock),
        mock.patch('django.contrib.contenttypes.models.ContentType.objects.get_for_model', return_value=mock.Mock()),
    ):
        mock_qs.annotate.return_value = mock_qs
        CustomQuerySet.include_attrs(mock_qs, 'foo')
        mock_qs.prefetch_related.assert_called_with('attributes')
        mock_qs.annotate.assert_called()


def test_include_attrs_programming_error(test_model):
    mock_qs = mock.Mock(spec=CustomQuerySet)
    mock_qs.model = test_model
    mock_qs.prefetch_related.return_value = mock_qs

    mock_attribute = mock.Mock()
    mock_attribute.objects.filter.return_value.values_list.return_value = [1, 2]

    mock_attributetype = mock.Mock()

    def raise_exc(*a, **kw):  # noqa: ARG001
        raise ProgrammingError

    mock_attributetype.objects.get.side_effect = raise_exc

    with (
        mock.patch('domain.models.attribute.Attribute', mock_attribute),
        mock.patch('domain.models.attribute.AttributeType', mock_attributetype),
        mock.patch('domain.models.attribute.AttributeField', mock.Mock),
        mock.patch('domain.models.attribute.ListField', mock.Mock),
        mock.patch('django.contrib.contenttypes.models.ContentType.objects.get_for_model', return_value=mock.Mock()),
    ):
        mock_qs.annotate.return_value = mock_qs
        CustomQuerySet.include_attrs(mock_qs, 'foo')
        mock_qs.prefetch_related.assert_called_with('attributes')
        mock_qs.annotate.assert_called()


def test_include_attrs_uses_parent_model_for_mti():
    """Test that include_attrs uses the parent model if MTI with UuidMixin."""

    class DummyUuidMixin:
        pass

    class Parent(DummyUuidMixin):
        __name__ = 'Parent'

    class Child(Parent):
        __name__ = 'Child'
        _meta = mock.Mock()
        # Simulate get_parent_list returning Parent
        _meta.get_parent_list.return_value = [Parent]

    mock_qs = mock.Mock(spec=CustomQuerySet)
    mock_qs.model = Child
    mock_qs.prefetch_related.return_value = mock_qs

    mock_attribute = mock.Mock()
    mock_attribute.objects.filter.return_value.values_list.return_value = [1, 2]

    mock_attributetype = mock.Mock()
    mock_attributetype.objects.get.return_value.contenttypes.get.return_value.is_unique = True

    with (
        mock.patch('domain.models.attribute.Attribute', mock_attribute),
        mock.patch('domain.models.attribute.AttributeType', mock_attributetype),
        mock.patch('domain.models.attribute.AttributeField', mock.Mock),
        mock.patch('domain.models.attribute.ListField', mock.Mock),
        mock.patch('django.contrib.contenttypes.models.ContentType.objects.get_for_model', return_value=mock.Mock()),
        mock.patch('app.abstract.custom_manager.UuidMixin', DummyUuidMixin),
    ):
        mock_qs.annotate.return_value = mock_qs
        CustomQuerySet.include_attrs(mock_qs, 'foo')
        # The filter should have been called with Parent as the model
        called_kwargs = mock_attribute.objects.filter.call_args[1]
        assert f'domain_{Parent.__name__.lower()}_related' in called_kwargs
        mock_qs.prefetch_related.assert_called_with('attributes')
        mock_qs.annotate.assert_called()


@pytest.mark.parametrize(
    ('debug', 'env', 'should_fallback'),
    [
        (True, 'development', True),
        (False, 'production', True),
        (False, 'staging', True),
        (False, 'other', False),
    ],
)
def test_filter_tenant_runtimeerror_fallback(debug, env, should_fallback):
    # Setup
    manager = custom_manager.CustomManager()
    manager.model = type('Dummy', (), {'is_tenanted': True})  # minimal model with is_tenanted

    qs = mock.Mock()

    # Simulate qs.filter raising RuntimeError on first call, then returning qs on fallback
    def filter_side_effect(*args, **kwargs):
        if args or kwargs:
            if should_fallback:
                return qs
            raise RuntimeError
        return qs

    qs.filter.side_effect = filter_side_effect

    # Patch get_current_tenant to return a dummy with pk
    with (
        mock.patch.object(custom_manager, 'get_current_tenant', return_value=mock.Mock(pk=1)),
        mock.patch.object(custom_manager, 'CustomQuerySet', return_value=qs),
        mock.patch.object(custom_manager.settings, 'DEBUG', debug),
        mock.patch.dict(os.environ, {'ENV': env}),
    ):
        if should_fallback:
            result = manager.get_queryset()
            assert result is qs
            assert qs.filter.call_count >= 1
        else:
            with pytest.raises(RuntimeError):
                manager.get_queryset()


def test_unscoped_returns_queryset():
    manager = custom_manager.CustomManager()
    # Assign a dummy model and db
    manager.model = type('Dummy', (), {})
    manager._db = 'default'  # noqa: SLF001
    qs = manager.unscoped()
    from django.db.models import QuerySet

    assert isinstance(qs, QuerySet)
    assert qs.model is manager.model
    assert qs.db == manager._db  # noqa: SLF001
