"""Widgets for team extension."""

from django.forms import Media
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

    @cached_property
    def media(self):
        multi_media = super().media
        return Media(
            js=['js/user-select-widget.js', *multi_media._js],  # noqa: SLF001
            css={'all': ['css/user-select-widget.css', *multi_media._css['all']]},  # noqa: SLF001
        )


class TeamMemberSelect(UserSelect):
    @cached_property
    def media(self):
        multi_media = super().media
        return Media(
            js=[*multi_media._js, 'js/team-select-widget.js'],  # noqa: SLF001
            css=multi_media._css,  # noqa: SLF001
        )
