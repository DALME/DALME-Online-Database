"""Configure pytest for the tests.web module."""

import io
from pathlib import Path

import pytest
from django_tenants.utils import schema_context
from faker import Faker
from PIL import Image

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.db import connection

from tenants.models import Domain, Tenant


@pytest.fixture(scope='session', autouse=True)
def setup_tenant_schema(django_db_setup, django_db_blocker):  # noqa: ARG001
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
                    for row in connection.cursor()
                    .execute('SELECT schema_name FROM information_schema.schemata')
                    .fetchall()
                ]:
                    connection.cursor().execute(f'CREATE SCHEMA "{schema_name}"')
                    call_command(
                        'migrate_schemas', tenant=True, schema_name=schema_name, interactive=False, verbosity=0
                    )


@pytest.fixture
def team_member(factories):
    """Inject a regular team member."""
    return factories.team_members.create()


@pytest.fixture
def avatar_image():
    """Inject an avatar image."""
    fake = Faker()
    filename = fake.file_name(category='image', extension='png')

    with io.BytesIO() as buffer:
        image = Image.new('RGBA', size=(50, 50), color=(155, 0, 0))
        image.save(buffer, 'png')
        buffer.name = filename
        buffer.seek(0)
        image_file = SimpleUploadedFile(name=filename, content=buffer.getvalue(), content_type='image/png')

        # Manifest handling and filename collisions can cause a non-deterministic
        # hash to be added to the filename, so we retrieve the *actual* name next.
        filename = Path(image_file.name).name

        return image_file
