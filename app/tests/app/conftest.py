"""Configure pytest for the tests.app module."""

import pytest

from app.abstract.custom_manager import CustomManager


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
