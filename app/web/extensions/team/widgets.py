"""Widgets for team extension."""

from django.forms import ClearableFileInput, Media
from django.utils.functional import cached_property

from web.extensions.extras.widgets import MultiSelect


class UserSelect(MultiSelect):
    def __init__(self, handle_form_fields=False, **kwargs):
        super().__init__(**kwargs)
        self.handle_form_fields = handle_form_fields
        self.container_classes.append('select-user')

    def build_attrs(self, *args, **kwargs):
        attrs = super().build_attrs(*args, **kwargs)
        if self.handle_form_fields:
            attrs['data-handle-form-fields'] = True
        return attrs

    def append_option_attrs(self, value, option_attrs):
        """Append user data items to option attributes."""
        if value:
            opt_id = value if isinstance(value, str | int) else value.value
            instance = self.queryset.get(id=opt_id)
            option_attrs.update(
                {
                    'avatar': instance.avatar,
                    'name': instance.full_name,
                    'username': instance.username,
                }
            )
        return option_attrs

    @cached_property
    def media(self):
        multi_media = super().media
        return Media(
            js=['js/user-select-widget.js', *multi_media._js],  # noqa: SLF001
            css={'all': ['css/user-select-widget.css', *multi_media._css['all']]},  # noqa: SLF001
        )


class TeamMemberSelect(UserSelect):
    def append_option_attrs(self, value, option_attrs):
        """Append team member data items to option attributes."""
        if value:
            opt_id = value if isinstance(value, str | int) else value.value
            instance = self.queryset.get(id=opt_id)
            option_attrs.update(
                {
                    'avatar': instance.user.avatar if instance.user else None,
                    'name': instance.name,
                    'username': instance.user.username if instance.user else None,
                }
            )
        return option_attrs

    @cached_property
    def media(self):
        multi_media = super().media
        return Media(
            js=[*multi_media._js, 'js/team-select-widget.js'],  # noqa: SLF001
            css=multi_media._css,  # noqa: SLF001
        )


class AuthorSelect(UserSelect):
    @cached_property
    def media(self):
        multi_media = super().media
        return Media(
            js=[*multi_media._js, 'js/author-select-widget.js'],  # noqa: SLF001
            css=multi_media._css,  # noqa: SLF001
        )


class AvatarFileInput(ClearableFileInput):
    template_name = 'team/avatar_file_input.html'
    input_text = 'Upload avatar'

    @cached_property
    def media(self):
        multi_media = super().media
        return Media(
            js=[*multi_media._js],  # noqa: SLF001
            css={'all': ['css/avatar-file-widget.css']},
        )
