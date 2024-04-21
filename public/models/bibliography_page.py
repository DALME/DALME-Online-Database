"""Model bibliography page data."""

from wagtail.admin.panels import FieldPanel

from public.models.base_page import BasePage


class Bibliography(BasePage):
    parent_page_types = ['public.Section']
    subpage_types = ['public.Flat']
    page_description = 'A flat page that can include one or many bibliographies.'

    metadata_panels = [
        *BasePage.metadata_panels,
        FieldPanel('short_title'),
    ]
