"""Configure pytest for the tests.app module."""

import pytest

from django.db import connection, models

from app.abstract.custom_manager import CustomManager
from app.abstract.owned_mixin import OwnedMixin


@pytest.fixture
def mock_model():
    class Meta:
        @staticmethod
        def get_parent_list():
            return []

    class DummyModel:
        _meta = Meta()
        __name__ = 'DummyModel'
        is_tenanted = True

        @staticmethod
        def attribute_list():
            return ['foo', 'bar']

    return DummyModel


@pytest.fixture
def custom_manager_instance():
    return CustomManager()


@pytest.fixture
def dummy_attribute_field():
    class DummyAttributeField:
        pass

    return DummyAttributeField


@pytest.fixture
def dummy_list_field():
    class DummyListField:
        def __init__(self, *a, **kw):
            pass

    return DummyListField


@pytest.fixture
def test_model():
    # Concrete model for testing
    class TestModel(OwnedMixin):
        name = models.CharField(max_length=100)

        class Meta:
            app_label = 'abstract'

    with connection.schema_editor() as schema_editor:
        schema_editor.create_model(TestModel)

    return TestModel


@pytest.fixture
def test_model_instance(test_model):
    return test_model(name='test')
