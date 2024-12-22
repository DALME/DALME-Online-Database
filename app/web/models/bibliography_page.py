"""Model bibliography page data."""

from wagtail.admin.panels import FieldPanel

from web.models.base_page import BasePage


class Bibliography(BasePage):
    template = 'bibliography.html'
    parent_page_types = ['web.Section']
    subpage_types = ['web.Flat']
    page_description = 'A flat page that can include one or many bibliographies.'

    metadata_panels = [
        *BasePage.metadata_panels,
        FieldPanel('short_title'),
    ]
