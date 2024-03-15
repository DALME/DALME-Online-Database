"""Model section page data."""

from wagtail.admin.panels import FieldPanel

from public.models.base_page import BasePage


class Section(BasePage):
    parent_page_types = ['public.Home']
    subpage_types = [
        'public.Flat',
        'public.Bibliography',
    ]

    content_panels = [*BasePage.content_panels, FieldPanel('short_title')]
