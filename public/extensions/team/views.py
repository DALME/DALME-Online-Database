"""Views for team extension."""

from wagtail.admin.panels import FieldPanel, FieldRowPanel
from wagtail.admin.ui.tables import UpdatedAtColumn
from wagtail.admin.viewsets.base import ViewSetGroup
from wagtail.admin.viewsets.model import ModelViewSet

from .models import TeamMember, TeamRole


class TeamRoleViewSet(ModelViewSet):
    model = TeamRole
    icon = 'user-tag'
    menu_label = 'Team Roles'
    menu_name = 'team_roles'
    menu_order = 900
    list_display = ['id', 'role', 'parent', UpdatedAtColumn()]
    columns = ['Id', 'Role', 'Parent', 'Updated']
    list_filter = ['role']
    search_fields = ['role']

    panels = [
        FieldPanel('role'),
        FieldPanel('parent'),
    ]


class TeamMemberViewSet(ModelViewSet):
    model = TeamMember
    icon = 'user'
    menu_label = 'Team Members'
    menu_name = 'team_members'
    menu_order = 900
    list_display = ['name', 'user', 'title', 'affiliation', UpdatedAtColumn()]
    columns = ['Name', 'User', 'Title(s)', 'Affiliation', 'Updated']
    list_filter = ['name', 'title', 'affiliation']
    search_fields = ['name', 'title', 'affiliation', 'biography']

    panels = [
        FieldRowPanel(
            [
                FieldPanel('name', classname='col8'),
                FieldPanel('user', classname='col4'),
            ],
        ),
        FieldRowPanel(
            [
                FieldPanel('title', classname='col8'),
                FieldPanel('affiliation', classname='col4'),
            ],
        ),
        FieldRowPanel(
            [
                FieldPanel('roles', classname='col8'),
                FieldPanel('photo', classname='col4'),
            ],
        ),
        FieldPanel('biography'),
        FieldPanel('url'),
    ]


class TeamViewSetGroup(ViewSetGroup):
    menu_label = 'Team'
    menu_icon = 'people-group'
    items = (TeamMemberViewSet, TeamRoleViewSet)
