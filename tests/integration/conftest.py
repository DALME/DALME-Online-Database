"""Configure pytest for the integration tests module."""
import pytest


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):  # noqa: ARG001,PT004
    pass


@pytest.mark.django_db()
@pytest.fixture(autouse=True)
def use_current_tenant():
    return None
