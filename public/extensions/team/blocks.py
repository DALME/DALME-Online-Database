"""Blocks for team extension."""

from wagtail import blocks
from wagtail.blocks.struct_block import StructBlockAdapter
from wagtail.images.blocks import ImageChooserBlock
from wagtail.telepath import register

from django import forms
from django.core.exceptions import ValidationError
from django.utils.functional import cached_property

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
    ('join-date-asc', 'Join date (oldest first)'),
    ('join-date-dsc', 'Join date (latest first)'),
]


def get_role_choices():
    return TeamRole.objects.values_list('id', 'role')


def get_member_choices():
    return TeamMember.objects.values_list('id', 'name')


class PersonBlock(blocks.StructBlock):
    name = blocks.CharBlock()
    job = blocks.CharBlock(required=False)
    institution = blocks.CharBlock(required=False)
    url = blocks.URLBlock(required=False)
    photo = ImageChooserBlock(required=False)

    class Meta:
        icon = 'person'
        template = 'person_block.html'


class TeamListStructValue(blocks.StructValue):
    def member_list(self):
        if self.get('members'):
            return TeamMember.objects.filter(id__in=self.get('members'))
        return TeamMember.objects.filter(roles=self.get('role'))


class TeamListBlock(blocks.StructBlock):
    mode = blocks.ChoiceBlock(
        label='List mode',
        choices=MODE_CHOICES,
        help_text='Select how you wish to define the list.',
    )
    order = blocks.ChoiceBlock(
        label='Order',
        choices=ORDER_CHOICES,
        default='name',
        help_text='Select how the list should be ordered.',
    )
    members = blocks.MultipleChoiceBlock(
        label='Members',
        choices=get_member_choices,
        required=False,
        widget=TeamMemberSelect(
            placeholder='Select members...',
            api_state='userSelectState',
        ),
        help_text='Manually select team members to include in the list.',
    )
    role = blocks.ChoiceBlock(
        label='Role',
        choices=get_role_choices,
        required=False,
        help_text='Select a role to define the list (all members with that role will be included).',
    )

    class Meta:
        value_class = TeamListStructValue
        label = 'Team List'
        icon = 'address-card'
        template = 'team_list_block.html'
        help_text = 'A list of team members to display.'
        form_classname = 'struct-block team-list-block'
        form_template = 'team_list_form.html'

    def clean(self, value):
        for name, val in value.items():
            if name == 'members' and isinstance(val, list) and len(val) == 1 and val[0] == '':
                value['members'] = None
        if not value.get('members') and not value.get('role'):
            error = 'Either a list of members or a role must be supplied.'
            raise ValidationError(error)
        return super().clean(value)


class TeamListBlockAdapter(StructBlockAdapter):
    js_constructor = 'publicteam.TeamListBlock'

    @cached_property
    def media(self):
        structblock_media = super().media
        return forms.Media(
            js=[*structblock_media._js, 'js/team-list-block.js'],  # noqa: SLF001
            css={'all': ['css/team-list-form.css']},
        )


register(TeamListBlockAdapter(), TeamListBlock)
