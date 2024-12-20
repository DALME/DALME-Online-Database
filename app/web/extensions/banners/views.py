"""Views for banners."""

from wagtail.admin.panels import FieldPanel, FieldRowPanel
from wagtail.admin.ui.tables import UpdatedAtColumn
from wagtail.admin.viewsets.model import ModelViewSet

from .models import Banner


class BannersViewSet(ModelViewSet):
    model = Banner
    icon = 'bullhorn'
    menu_label = 'Banners'
    menu_name = 'banners'
    menu_order = 900
    add_to_admin_menu = True
    list_display = ['title', 'start_date', 'end_date', UpdatedAtColumn()]
    list_filter = ['title', 'info']
    search_fields = ['title', 'info']

    panels = [
        FieldRowPanel(
            [
                FieldPanel('title', classname='col8'),
                FieldPanel('show_title', classname='col1'),
                FieldPanel('color', classname='col3'),
            ],
            classname='field-row-panel',
        ),
        FieldPanel('info'),
        FieldPanel('page'),
        FieldPanel('url'),
        FieldRowPanel(
            [
                FieldPanel('start_date'),
                FieldPanel('end_date'),
            ],
            heading='Display dates',
            classname='field-row-panel',
        ),
    ]
