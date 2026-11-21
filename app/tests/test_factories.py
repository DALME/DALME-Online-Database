"""Test the conventions every model factory follows."""

import importlib
import pkgutil

import factory
import pytest

from django.core.exceptions import FieldDoesNotExist

import tests.factories


def all_factories():
    for module_info in pkgutil.walk_packages(tests.factories.__path__, f'{tests.factories.__name__}.'):
        module = importlib.import_module(module_info.name)
        for value in vars(module).values():
            if isinstance(value, type) and issubclass(value, factory.Factory) and value.__module__ == module.__name__:
                yield value


def has_choices(factory_class, name):
    model = factory_class._meta.get_model_class()  # noqa: SLF001
    try:
        return bool(model._meta.get_field(name).choices)  # noqa: SLF001
    except (AttributeError, FieldDoesNotExist):
        return False


def test_no_factory_declares_a_fixed_string():
    # A field with choices may name one deliberately; free text must vary.
    fixed = [
        f'{factory_class.__name__}.{name}'
        for factory_class in all_factories()
        for name, declaration in factory_class._meta.declarations.items()  # noqa: SLF001
        if isinstance(declaration, str) and not has_choices(factory_class, name)
    ]

    assert fixed == []


@pytest.mark.django_db
def test_each_record_gets_its_own_name(factories):
    first, second = factories.records.create_batch(2)

    assert first.name != second.name


TENANTED = ['task_lists', 'tasks', 'collections', 'options_values']


@pytest.mark.django_db
@pytest.mark.parametrize('resource', TENANTED)
def test_tenanted_factories_take_the_bound_tenant(resource, factories, current_tenant):
    instance = getattr(factories, resource).create()

    assert instance.tenant.pk == current_tenant.pk


@pytest.mark.django_db
@pytest.mark.parametrize('resource', TENANTED)
def test_tenanted_factories_take_an_explicit_tenant(resource, factories, current_tenant, other_tenant):  # noqa: ARG001
    instance = getattr(factories, resource).create(tenant=other_tenant)

    assert instance.tenant.pk == other_tenant.pk


@pytest.mark.django_db
def test_a_task_shares_its_lists_tenant(factories, current_tenant, other_tenant):  # noqa: ARG001
    task = factories.tasks.create(tenant=other_tenant)

    assert task.task_list.tenant.pk == other_tenant.pk


@pytest.mark.django_db
def test_tenanted_factories_need_a_tenant(factories):
    with pytest.raises(RuntimeError, match='Bind a tenant'):
        factories.task_lists.create()
