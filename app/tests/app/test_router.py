"""Tests for the database router in the application."""

import pytest


def test_db_for_read_with_in_db(db_router, test_model):
    model = test_model('custom_db')
    assert db_router.db_for_read(model) == 'custom_db'


def test_db_for_read_without_in_db(db_router):
    class NoInDbMeta:
        pass

    class NoInDbModel:
        _meta = NoInDbMeta()

    model = NoInDbModel()
    assert db_router.db_for_read(model) is None


def test_db_for_write_with_in_db(db_router, test_model):
    model = test_model('write_db')
    assert db_router.db_for_write(model) == 'write_db'


def test_db_for_write_without_in_db(db_router):
    class NoInDbMeta:
        pass

    class NoInDbModel:
        _meta = NoInDbMeta()

    model = NoInDbModel()
    assert db_router.db_for_write(model) is None


@pytest.mark.parametrize(
    ('model_db', 'db', 'expected'),
    [
        ('sync_db', 'sync_db', True),
        ('other_db', 'sync_db', False),
        (None, 'default', True),
        (None, 'not_default', False),
    ],
)
def test_allow_syncdb(db_router, model_db, db, expected, test_model):
    model = test_model(model_db) if model_db is not None else test_model()
    assert db_router.allow_syncdb(db, model) == expected
