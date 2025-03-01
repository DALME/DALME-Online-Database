"""Views for team extension."""

from wagtail.admin.panels import FieldPanel, FieldRowPanel, ObjectList, TabbedInterface
from wagtail.admin.ui.tables import Column, UpdatedAtColumn
from wagtail.admin.views.account import AccountView, AvatarSettingsPanel
from wagtail.admin.views.generic.models import IndexView
from wagtail.admin.viewsets.base import ViewSetGroup
from wagtail.admin.viewsets.model import ModelViewSet

from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.utils.functional import cached_property
from django.views.decorators.debug import sensitive_post_parameters

from web.extensions.extras.widgets import MultiSelect

from .forms import TeamAvatarPreferencesForm, UserAvatarPreferencesForm
from .models import TeamMember, TeamRole
from .widgets import AvatarFileInput, UserSelect


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
    list_display = ['avatar', 'name', 'user', 'title', 'affiliation']
    list_filter = ['name', 'title', 'affiliation']
    search_fields = ['name', 'title', 'affiliation', 'biography']
    index_results_template_name = 'team/team_list/index_results.html'
    ordering = ['name']

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
                        api_state='userSelectState',
                        queryset=get_user_model().objects.all(),
                    ),
                ),
                FieldPanel('name', classname='col8'),
            ],
            heading='ID',
            classname='field-row-panel collapse-help',
        ),
        FieldRowPanel(
            [
                FieldPanel('roles', classname='col9', widget=MultiSelect(placeholder='Select roles...')),
                FieldPanel('avatar', classname='col3', widget=AvatarFileInput),
            ],
            heading='Roles and avatar',
            classname='field-row-panel collapse-help',
        ),
    ]
    professional_panels = [
        FieldRowPanel(
            [
                FieldPanel('title', classname='col7'),
                FieldPanel('affiliation', classname='col5'),
            ],
            heading='Affiliation',
            classname='field-row-panel collapse-help',
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


class UserAvatarSettingsPanel(AvatarSettingsPanel):
    title = 'User picture'
    form_class = UserAvatarPreferencesForm
    form_object = 'user'


class TeamAvatarSettingsPanel(AvatarSettingsPanel):
    name = 'teamavatar'
    title = 'Team member picture'
    order = 301
    template_name = 'team/avatar_admin_panel.html'
    form_class = TeamAvatarPreferencesForm
    form_object = 'profile'  # will use third argument to form class


@method_decorator(sensitive_post_parameters(), name='post')
class TeamAccountView(AccountView):
    """Override the account view to prevent the default avatar panel from saving alongside our panel override."""

    def get_panels(self):
        panels = [panel for panel in super().get_panels() if panel.name != 'avatar']
        panels.append(UserAvatarSettingsPanel(self.request, self.request.user, {}))
        tm = TeamMember.objects.filter(user=self.request.user)
        if tm.exists():
            panels.append(TeamAvatarSettingsPanel(self.request, self.request.user, tm.first()))
        return panels
