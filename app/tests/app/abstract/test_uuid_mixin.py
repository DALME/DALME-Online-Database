"""Unit tests for UUID model and mixin."""

import uuid

import pytest

from django.db import models

from app.abstract.uuid_mixin import UuidMixin


@pytest.mark.django_db
def test_uuid_is_assigned_on_creation(factories):
    obj = factories.uuid_models.create(name='Test_creation')
    assert obj.id is not None
    assert isinstance(obj.id, uuid.UUID)


@pytest.mark.django_db
def test_uuid_is_unique(factories):
    obj1 = factories.uuid_models.create(name='Test_unique1')
    obj2 = factories.uuid_models.create(name='Test_unique2')
    assert obj1.id != obj2.id


@pytest.mark.django_db
def test_uuid_field_properties():
    field = UuidMixin._meta.get_field('id')  # noqa: SLF001
    assert isinstance(field, models.UUIDField)
    assert field.primary_key is True
    assert field.editable is False
    assert field.db_index is True
