"""Configure pytest for the tests.app module."""

from types import SimpleNamespace
from unittest import mock

import pytest

from app import access_policies
from app.abstract.custom_manager import CustomManager
from app.router import ModelDatabaseRouter


@pytest.fixture
def test_model():
    class Meta:
        def __init__(self, in_db=None):
            if in_db is not None:
                self.in_db = in_db

        @staticmethod
        def get_parent_list():
            return []

    class Model:
        _meta = Meta()
        __name__ = 'Model'
        is_tenanted = True

        def __init__(self, in_db=None):
            self._meta = Meta(in_db)

        @staticmethod
        def attribute_list():
            return ['foo', 'bar']

    return Model


@pytest.fixture
def custom_manager_instance():
    return CustomManager()


@pytest.fixture
def db_router():
    return ModelDatabaseRouter()


@pytest.fixture
def mock_request(user):
    req = mock.Mock()
    req.user = user
    req.access_enforcement = None
    return req


@pytest.fixture
def mock_object_1():
    return SimpleNamespace(id=1)


@pytest.fixture
def mock_object_2():
    return SimpleNamespace(id=2)


@pytest.fixture
def mock_view_list(mock_object_1, mock_object_2):
    view = mock.Mock()
    view.action = 'list'
    view.get_queryset.return_value = [mock_object_1, mock_object_2]
    view.detail = False
    view.request = mock.Mock()
    view.request.data = {}
    view.kwargs = {}
    del view.object
    return view


@pytest.fixture
def mock_view_detail(mock_object_1):
    view = mock.Mock()
    view.action = 'detail'
    view.object = mock_object_1
    view.detail = True
    view.request = mock.Mock()
    view.request.data = {}
    view.kwargs = {}
    return view


@pytest.fixture
def base_policy():
    # Reset class variables for isolation
    access_policies.BaseAccessPolicy.permissions = {}
    access_policies.BaseAccessPolicy.targets = []
    return access_policies.BaseAccessPolicy()
