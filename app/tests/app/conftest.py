"""Configure pytest for the tests.app module."""

import pytest

from app.abstract.custom_manager import CustomManager

# @pytest.fixture(scope='session', autouse=True)
# def set_test_model(django_db_setup, django_db_blocker):
#     with django_db_blocker.unblock(), schema_context('public'), connection.schema_editor() as schema_editor:
#         if (
#             not connection.cursor()
#             .execute("SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name='abstract_testmodel')")
#             .fetchone()[0]
#         ):
#             # Create the table if it does not exist
#             schema_editor.create_model(TestModel)


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
