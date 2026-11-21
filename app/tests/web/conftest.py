"""Configure pytest for the tests.web module."""

import io
from pathlib import Path

import pytest
from django_tenants.utils import tenant_context
from faker import Faker
from PIL import Image

from django.core.files.uploadedfile import SimpleUploadedFile

from web.models import Essay, FeaturedInventory, FeaturedObject


@pytest.fixture
def project_schema(test_tenant):
    """Bind the test project's schema, where its CMS lives."""
    with tenant_context(test_tenant):
        yield test_tenant


@pytest.fixture
def team_member(factories, project_schema):  # noqa: ARG001
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


@pytest.fixture
def featured_pages(factories, project_schema):  # noqa: ARG001
    """Inject a queryset of featured essays, objects, and inventories."""
    essays = factories.essay_pages.create_batch(3)
    objects = factories.featured_object_pages.create_batch(3)
    inventories = factories.featured_inventory_pages.create_batch(3)

    return [*essays, *objects, *inventories]


@pytest.fixture
def featured_pages_qs(project_schema):  # noqa: ARG001
    """Inject a queryset of featured pages."""
    return FeaturedInventory.objects.all().union(FeaturedObject.objects.all(), Essay.objects.all())


@pytest.fixture
def test_site(factories, project_schema):  # noqa: ARG001
    home_page = factories.home_pages.create()
    factories.flat_pages.create(parent=home_page)  # home page child (i.e. content)
    site = factories.sites.create(root_page=home_page)
    section = factories.pages_sections.create(parent=home_page)
    factories.flat_pages.create_batch(3, parent=section)
    return site
