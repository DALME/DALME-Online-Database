"""Forms for team extensions."""

from wagtail.admin.forms.account import AvatarPreferencesForm

from django.contrib.auth import get_user_model


class TeamAvatarPreferencesForm(AvatarPreferencesForm):
    class Meta:
        model = get_user_model()
        fields = ['avatar']
