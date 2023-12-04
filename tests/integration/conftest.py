"""Configure pytest for the tests.integration module."""
import pytest


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):  # noqa: ARG001,PT004
    pass
