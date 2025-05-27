"""Configure pytest for the tests.web module."""

import io
from pathlib import Path

import pytest
from faker import Faker
from PIL import Image

from django.core.files.uploadedfile import SimpleUploadedFile


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
