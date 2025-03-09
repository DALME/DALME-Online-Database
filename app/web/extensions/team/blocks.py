"""Blocks for team extension."""

from wagtail import blocks
from wagtail.blocks.struct_block import StructBlockAdapter
from wagtail.telepath import register

from django import forms
from django.core.exceptions import ValidationError
from django.db.models import OuterRef, Subquery
from django.utils.functional import cached_property

from web.extensions.extras.widgets import CustomSelect

from .models import TeamMember, TeamRole
from .widgets import TeamMemberSelect

MODE_CHOICES = [
    ('members', 'Manual list'),
    ('role', 'Role-based list'),
]

ORDER_CHOICES = [
    ('name', 'Name'),
    ('role', 'Role'),
    ('affiliation', 'Affiliation'),
    ('user__date_joined', 'Join date (oldest first)'),
    ('-user__date_joined', 'Join date (latest first)'),
]


def get_role_choices():
    return TeamRole.objects.values_list('id', 'role')


def get_member_choices():
    return TeamMember.objects.values_list('id', 'name')


class TeamListStructValue(blocks.StructValue):
    def member_list(self):
        if self.get('members'):
            qs = TeamMember.objects.filter(id__in=self.get('members'))
            order = self.get('order')
            if order != 'role':
                return qs.order_by(order, 'name')
            roles = TeamRole.objects.filter(teammember=OuterRef('pk'))
            return qs.annotate(role=Subquery(roles.values('role')[:1])).order_by('-role', 'name')
        return TeamMember.objects.filter(roles=self.get('role')).order_by(self.get('order'), 'name')


class TeamListBlock(blocks.StructBlock):
    mode = blocks.ChoiceBlock(
        label='List mode',
        choices=MODE_CHOICES,
        help_text='Select how you wish to define the list.',
        widget=CustomSelect,
    )
    order = blocks.ChoiceBlock(
        label='Order',
        choices=ORDER_CHOICES,
        default='name',
        help_text='Select how the list should be ordered.',
        widget=CustomSelect,
    )
    members = blocks.MultipleChoiceBlock(
        label='Members',
        choices=get_member_choices,
        required=False,
        widget=TeamMemberSelect(
            placeholder='Select members...',
            api_state='userSelectState',
            queryset=TeamMember.objects.all(),
        ),
        help_text='Manually select team members to include in the list.',
    )
    role = blocks.ChoiceBlock(
        label='Role',
        choices=get_role_choices,
        required=False,
        help_text='Select a role to define the list (all members with that role will be included).',
        widget=CustomSelect,
    )

    class Meta:
        value_class = TeamListStructValue
        label = 'Team List'
        icon = 'address-card'
        template = 'team/team_list_block.html'
        form_classname = 'struct-block team-list-block'
        form_template = 'team/team_list_form.html'

    def clean(self, value):
        for name, val in value.items():
            if name == 'members' and isinstance(val, list) and len(val) == 1 and val[0] == '':
                value['members'] = None
        if not value.get('members') and not value.get('role'):
            error = 'Either a list of members or a role must be supplied.'
            raise ValidationError(error)
        return super().clean(value)


class TeamListBlockAdapter(StructBlockAdapter):
    js_constructor = 'webteam.TeamListBlock'

    @cached_property
    def media(self):
        structblock_media = super().media
        return forms.Media(
            js=[
                *structblock_media._js,  # noqa: SLF001
                'js/team-list-form.js',
            ],
            css={'all': ['css/team-list-form.css']},
        )


register(TeamListBlockAdapter(), TeamListBlock)
