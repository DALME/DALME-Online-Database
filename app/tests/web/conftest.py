"""Configure pytest for the tests.web module."""

import io
from pathlib import Path

import pytest
from faker import Faker
from PIL import Image

from django.core.files.uploadedfile import SimpleUploadedFile

from web.models import Essay, FeaturedInventory, FeaturedObject


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


@pytest.fixture
def featured_pages(factories):
    """Inject a queryset of featured essays, objects, and inventories."""
    essays = factories.essay_pages.create_batch(3)
    objects = factories.featured_object_pages.create_batch(3)
    inventories = factories.featured_inventory_pages.create_batch(3)

    return [*essays, *objects, *inventories]


@pytest.fixture
def featured_pages_qs():
    """Inject a queryset of featured pages."""
    return FeaturedInventory.objects.all().union(FeaturedObject.objects.all(), Essay.objects.all())


@pytest.fixture
def test_site(factories):
    home_page = factories.home_pages.create()
    factories.flat_pages.create(parent=home_page, slug='home')  # home page child (i.e. content)
    site = factories.sites.create(root_page=home_page)
    section1 = factories.pages_sections.create(title='Section 1', parent=home_page, slug='section-1')
    factories.flat_pages.create_batch(3, parent=section1)
    return site
