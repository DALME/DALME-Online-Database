"""Model section page data."""

from wagtail.admin.panels import FieldPanel

from web.extensions.gradients.models import GradientMixin
from web.models.base_page import BasePage


class Section(BasePage, GradientMixin):
    parent_page_types = ['web.Home']
    subpage_types = [
        'web.Bibliography',
        'web.Flat',
        'web.People',
    ]
    page_description = 'Defines a menu section. Can have a gradient (used by child pages), but no other content.'

    content_panels = None
    metadata_panels = [
        *GradientMixin.metadata_panels,
        FieldPanel('short_title'),
    ]
