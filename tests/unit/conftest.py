"""Configure pytest for the unit tests module."""
from unittest import mock

import pytest

from dalme_app.models import Tenant


@pytest.fixture(scope='session', autouse=True)
def mock_get_current_tenant():
    with mock.patch('dalme_app.tenant.get_current_tenant') as mock_func:
        mock_func.return_value = mock.MagicMock(spec=Tenant)
        yield mock_func
