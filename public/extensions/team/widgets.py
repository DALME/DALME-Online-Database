"""Widgets for team extension."""

from django.forms import Media
from django.utils.functional import cached_property

from public.extensions.extras.widgets import MultiSelect

AVATAR = '<div class="avatar-bg" style="background: center/cover url({});"></div>'
PLACEHOLDER = '<svg class="icon icon-user user-placeholder" aria-hidden="true"><use href="#icon-user"></use></svg>'


class UserSelect(MultiSelect):
    def __init__(self, handle_form_fields=False, **kwargs):
        super().__init__(**kwargs)
        self.handle_form_fields = handle_form_fields
        self.container_classes.append('select-user')
        self.option_data = {}

    def format_label(self, value, label):  # noqa: ARG002
        if isinstance(value, str):
            return f'<div class="user-option"><div class="text-placeholder">{self.placeholder}</div></div>'

        instance = value.instance
        full_name = instance.wagtail_userprofile.profile.full_name
        username = instance.username
        image = instance.wagtail_userprofile.profile.profile_image
        avatar = AVATAR.format(image) if image else PLACEHOLDER

        self.option_data[instance.id] = {
            'name': full_name,
            'username': username,
            'avatar': image,
        }

        return (
            f'<div class="user-option">{avatar}<div class="user-label">{full_name} <span>{username}</span></div></div>'
        )

    def get_option_data(self):
        """Get option data function to be overriden by subclasses."""
        return {
            'options': self.option_list,
            'data': self.option_data,
        }

    def build_attrs(self, *args, **kwargs):
        attrs = super().build_attrs(*args, **kwargs)
        if self.handle_form_fields:
            attrs['data-handle-form-fields'] = True
        return attrs

    @cached_property
    def media(self):
        multi_media = super().media
        return Media(
            js=['js/user-select-widget.js', *multi_media._js],  # noqa: SLF001
            css={'all': ['css/user-select-widget.css', *multi_media._css['all']]},  # noqa: SLF001
        )
