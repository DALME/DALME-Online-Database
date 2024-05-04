"""Views for team extension."""

from wagtail.admin.panels import FieldPanel, FieldRowPanel, ObjectList, TabbedInterface
from wagtail.admin.ui.tables import Column, UpdatedAtColumn
from wagtail.admin.views.generic.models import IndexView
from wagtail.admin.viewsets.base import ViewSetGroup
from wagtail.admin.viewsets.model import ModelViewSet

from django.utils.functional import cached_property

from public.extensions.extras.widgets import MultiSelect

from .models import TeamMember, TeamRole
from .widgets import UserSelect


class TeamRoleViewSet(ModelViewSet):
    model = TeamRole
    icon = 'user-tag'
    menu_label = 'Roles'
    menu_name = 'team_roles'
    menu_order = 900
    list_display = ['role', 'description', 'parent', UpdatedAtColumn()]
    list_filter = ['role']
    search_fields = ['role']

    panels = [
        FieldPanel('role'),
        FieldPanel('parent'),
    ]


class TeamMemberIndexView(IndexView):
    @cached_property
    def columns(self):
        columns = []
        for i, field in enumerate(self.list_display):
            if isinstance(field, Column):
                column = field
            elif i == 1:
                column = self._get_title_column(field)
            else:
                column = self._get_custom_column(field)
            columns.append(column)

        return columns


class TeamMemberViewSet(ModelViewSet):
    model = TeamMember
    icon = 'user'
    menu_label = 'Members'
    menu_name = 'team_members'
    menu_order = 900
    index_view_class = TeamMemberIndexView
    list_display = ['photo', 'name', 'user', 'title', 'affiliation']
    list_filter = ['name', 'title', 'affiliation']
    search_fields = ['name', 'title', 'affiliation', 'biography']
    index_results_template_name = 'team_list/index_results.html'

    general_panels = [
        FieldRowPanel(
            [
                FieldPanel(
                    'user',
                    classname='col4',
                    widget=UserSelect(
                        placeholder='Select user...',
                        handle_form_fields=True,
                        multiselect=False,
                        use_state='userSelectState',
                    ),
                ),
                FieldPanel('name', classname='col8'),
            ],
            heading='ID',
            classname='field-row-panel',
        ),
        FieldRowPanel(
            [
                FieldPanel('roles', classname='col8', widget=MultiSelect(placeholder='Select roles...')),
                FieldPanel('photo', classname='col4'),
            ],
            heading='Roles and photo',
            classname='field-row-panel',
        ),
    ]
    professional_panels = [
        FieldRowPanel(
            [
                FieldPanel('title', classname='col8'),
                FieldPanel('affiliation', classname='col4'),
            ],
            heading='Affiliation',
            classname='field-row-panel',
        ),
        FieldPanel('url'),
    ]
    bio_panels = [FieldPanel('biography')]

    edit_handler = TabbedInterface(
        [
            ObjectList(general_panels, heading='General'),
            ObjectList(professional_panels, heading='Professional'),
            ObjectList(bio_panels, heading='Biography'),
        ]
    )


class TeamViewSetGroup(ViewSetGroup):
    menu_label = 'Team'
    menu_icon = 'people-group'
    items = (TeamMemberViewSet, TeamRoleViewSet)
