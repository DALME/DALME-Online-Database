"""Configure pytest for the tests.unit module."""

from unittest import mock

import pytest

from ida.models import Tenant


@pytest.fixture(scope='session', autouse=True)
def mock_get_current_tenant():
    with mock.patch('ida.tenant.get_current_tenant') as mock_func:
        mock_func.return_value = mock.MagicMock(spec=Tenant)
        yield mock_func
