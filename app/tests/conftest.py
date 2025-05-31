"""Configure pytest for the tests module."""

import uuid

import pytest
from django_tenants.utils import schema_context
from rest_framework.test import APIRequestFactory

from django.conf import settings
from django.core.management import call_command
from django.db import connections

from app.settings import TenantTypes
from tenants.models import Domain, Tenant

from tests.factories import ResourceFactory


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


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):  # noqa: ARG001
    """Create tenants and schemas and apply migrations."""
    tenants = settings.TENANTS()
    with django_db_blocker.unblock(), schema_context('public'):
        for tenant in tenants:
            domain, additional_domains, name, schema_name, is_primary, tenant_type = tenant.value

            if not Tenant.objects.filter(name=name).exists():
                tenant_obj = Tenant.objects.create(
                    name=name,
                    schema_name=schema_name,
                    tenant_type=tenant_type.value,
                )
                Domain.objects.create(
                    domain=domain,
                    tenant=tenant_obj,
                    is_primary=is_primary,
                )

                if schema_name not in [
                    row[0]
                    for row in connections['default']
                    .cursor()
                    .execute('SELECT schema_name FROM information_schema.schemata')
                    .fetchall()
                ]:
                    connections['default'].cursor().execute(f'CREATE SCHEMA "{schema_name}"')
                    call_command(
                        'migrate_schemas', tenant=True, schema_name=schema_name, interactive=False, verbosity=0
                    )


@pytest.fixture
def test_domain():
    """Inject a test domain."""
    return Domain.objects.filter(tenant__tenant_type=TenantTypes.PROJECT).first()


@pytest.fixture
def test_tenant(test_domain):
    """Inject a test tenant."""
    return test_domain.tenant


@pytest.fixture
def public_tenant():
    """Inject the public test tenant."""
    return Tenant.objects.get(schema_name='public')


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
        staff=True,
    )


@pytest.fixture
def superuser(factories, test_username, test_password):
    """Inject a superuser."""
    return factories.users.create(
        username=test_username,
        password=test_password,
        superuser=True,
    )


@pytest.fixture
def bare_agent(factories):
    """Inject a **Bare Agent**, ie. a person without a related user."""
    return factories.people(bare_agent=True)
