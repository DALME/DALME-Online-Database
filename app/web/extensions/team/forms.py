"""Forms for team extensions."""

from wagtail.admin.forms.account import AvatarPreferencesForm

from django.contrib.auth import get_user_model

from web.extensions.team.models import TeamMember


class UserAvatarPreferencesForm(AvatarPreferencesForm):
    class Meta:
        model = get_user_model()
        fields = ['avatar']


class TeamAvatarPreferencesForm(AvatarPreferencesForm):
    class Meta:
        model = TeamMember
        fields = ['avatar']
