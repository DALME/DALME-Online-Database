"""Configure pytest for the tests.app module."""

from unittest import mock

import pytest

from django.db import models

from app.abstract import custom_manager

# Patch imports for isolated testing
with mock.patch.dict(
    'sys.modules',
    {
        'app.context': mock.Mock(),
        'domain.models.attribute': mock.Mock(),
        'django.contrib.contenttypes.models': mock.Mock(),
        'django.contrib.postgres.expressions': mock.Mock(),
    },
):

    @pytest.fixture
    def mock_model():
        class MockMeta:
            def get_parent_list(self):
                return []

        class MockModel:
            _meta = MockMeta()
            __name__ = 'MockModel'

            @staticmethod
            def attribute_list():
                return ['foo', 'bar']

            is_tenanted = True

        return MockModel

    @pytest.fixture
    def custom_manager_instance(mock_model):
        class TestManager(custom_manager.CustomManager):
            model = mock_model
            _db = 'default'
            _queryset_class = models.QuerySet

            def _apply_rel_filters(self, queryset):
                return queryset

        return TestManager()
