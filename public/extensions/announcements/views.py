"""Views for announcements."""

from wagtail.admin.panels import FieldPanel, FieldRowPanel
from wagtail.admin.ui.tables import UpdatedAtColumn
from wagtail.admin.viewsets.model import ModelViewSet

from .models import Announcement


class AnnouncementsViewSet(ModelViewSet):
    model = Announcement
    icon = 'bullhorn'
    menu_label = 'Announcements'
    menu_name = 'announcements'
    menu_order = 900
    add_to_admin_menu = True
    list_display = ['id', 'title', 'start_date', 'end_date', UpdatedAtColumn()]
    columns = ['Id', 'Title', 'Start date', 'End Date', 'Updated']
    list_filter = ['title', 'info']
    search_fields = ['title', 'info']

    panels = [
        FieldRowPanel(
            [
                FieldPanel('title', classname='col8'),
                FieldPanel('show_title', classname='col1'),
                FieldPanel('color', classname='col3'),
            ],
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
        ),
    ]
