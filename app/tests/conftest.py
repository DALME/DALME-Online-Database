"""Configure pytest for the tests module."""

import uuid
from unittest import mock

import pytest
from rest_framework.test import APIRequestFactory

from django.conf import settings

from app.settings import TenantTypes
from oauth.models import User
from tenants.middleware import tenant_context_middleware
from tenants.models import Domain, Tenant

from tests.factories import ResourceFactory

MOCK_USER = mock.MagicMock(
    spec=User,
    id=1,
    username='hari.seldon',
)
MOCK_TENANT = mock.MagicMock(
    spec=Tenant,
    id=1,
    pk=1,
    name='DALME',
    tenant_type=TenantTypes.PROJECT,
    schema_name='dalme',
)
MOCK_DOMAIN = mock.MagicMock(
    spec=Domain,
    id=1,
    domain='dalme.localhost',
    is_primary=True,
    tenant=MOCK_TENANT,
)
MOCK_TENANT.domains.first.return_value = MOCK_DOMAIN
MOCK_TENANT.members.return_value = [MOCK_USER]
MOCK_TENANT.get_tenant_type.return_value = TenantTypes.PROJECT


def pytest_configure():
    """Configure pytest runs globally here."""
    settings.STORAGES['staticfiles'] = {'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage'}


def pytest_collection_modifyitems(items):
    """Automatically categorize tests if they rely on specific fixtures."""
    integration_fixtures = ['admin_client', 'client']
    property_fixtures = ['given']

    for item in items:
        is_unit: bool | None = None

        for fixture in integration_fixtures:
            if fixture in getattr(item, 'fixturenames', ()) or any(
                'django_db' in name for name in getattr(item, 'fixturenames', ())
            ):
                item.add_marker('integration')
                is_unit = False

        for fixture in property_fixtures:
            if fixture in getattr(item, 'fixturenames', ()):
                item.add_marker('property')
                is_unit = False

        if is_unit is None:
            item.add_marker('unit')


@pytest.fixture(scope='session', autouse=True)
def set_test_tenant():
    tenant_context_middleware._tenant.set(MOCK_TENANT)  # noqa: SLF001


@pytest.fixture
def test_domain():
    """Inject a test domain."""
    return MOCK_DOMAIN


@pytest.fixture
def arf():
    """Inject an instance of the DRF APIRequestFactory."""
    return APIRequestFactory()


@pytest.fixture
def test_username():
    """Inject a test username."""
    return 'hari.seldon'


@pytest.fixture
def test_email():
    """Inject a test email address."""
    return 'hari.seldon@streeling.edu'


@pytest.fixture
def test_password():
    """Inject a test password."""
    return 'password123'


@pytest.fixture
def test_uuid():
    """Inject a test UUID."""
    return uuid.UUID('00000000-0000-0000-0000-000000000000')


@pytest.fixture(scope='session')
def factories():
    """Inject a RESTFul factory interface."""
    return ResourceFactory()


@pytest.fixture
def user(factories, test_username, test_password):
    """Inject a regular user."""
    return factories.users.create(
        username=test_username,
        password=test_password,
    )


@pytest.fixture
def auth_user(client, factories, test_username, test_password):
    """Inject an authenticated user."""
    user = factories.users.create(
        username=test_username,
        password=test_password,
    )
    client.force_login(user)
    return user


@pytest.fixture
def admin_user(factories, test_username, test_password):
    """Inject a staff user."""
    return factories.users.create(
        username=test_username,
        password=test_password,
        is_staff=True,
    )


@pytest.fixture
def superuser(factories, test_username, test_password):
    """Inject a superuser."""
    return factories.users.create(
        username=test_username,
        password=test_password,
        is_staff=True,
        is_superuser=True,
    )


@pytest.fixture
def bare_agent(factories):
    """Inject a **Bare Agent**, ie. a person without a related user."""
    return factories.people(bare_agent=True)
