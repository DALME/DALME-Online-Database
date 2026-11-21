"""Test the header image styles template tag."""

from types import SimpleNamespace

import pytest

from web.extensions.gradients.models import Gradient
from web.extensions.gradients.templatetags.get_header_image_styles import get_header_image_styles

from tests.factories.fakers import fake


@pytest.mark.django_db
@pytest.mark.usefixtures('project_schema')
def test_a_page_takes_the_gradient_of_its_section(factories):
    gradient = Gradient.objects.create(
        colour_1=fake.hex_color(),
        colour_2=fake.hex_color(),
        angle=str(fake.random_int(max=359)),
    )
    home = factories.home_pages.create()
    section = factories.pages_sections.create(parent=home, gradient=gradient)
    page = factories.flat_pages.create(parent=section)
    image = SimpleNamespace(url=f'/media/{fake.file_name(category="image")}')

    styles = get_header_image_styles({'page': page}, image, 'center')

    assert styles.startswith(f'background-image: {gradient.css}, url({image.url})')
