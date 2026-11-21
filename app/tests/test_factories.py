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
