"""Configure fixtures for all tests in the module."""
import pytest


def pytest_collection_modifyitems(items):
    """Mark all tests depending on nature."""
    for item in items:
        if 'tests/integration' in item.path.as_posix():
            item.add_marker(pytest.mark.itegration)
        if 'tests/property' in item.path.as_posix():
            item.add_marker(pytest.mark.property)
        if 'tests/unit' in item.path.as_posix():
            item.add_marker(pytest.mark.unit)
