"""Model bibliography page data."""

from wagtail.admin.panels import FieldPanel

from public.models.base_page import BasePage


class Bibliography(BasePage):
    parent_page_types = ['public.Section']
    subpage_types = ['public.Flat']

    content_panels = [
        *BasePage.content_panels,
        FieldPanel('header_image'),
        FieldPanel('header_position'),
        FieldPanel('short_title'),
        FieldPanel('body'),
    ]
