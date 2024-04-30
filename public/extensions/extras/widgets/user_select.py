"""User select widget."""

import json

from django.forms import Media, Select

AVATAR = '<div class="avatar-bg" style="background: center/cover url({});"></div>'
PLACEHOLDER = '<svg class="icon icon-user user-placeholder" aria-hidden="true"><use href="#icon-user"></use></svg>'


class UserSelect(Select):
    def __init__(self, attrs=None, choices=(), handle_form_fields=False):
        super().__init__(attrs, choices)
        if handle_form_fields:
            self.option_data = {}
            self.handle_form_fields = True

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):  # noqa: PLR0913
        index = str(index) if subindex is None else '%s_%s' % (index, subindex)  # noqa: UP031
        option_attrs = self.build_attrs(self.attrs, attrs) if self.option_inherits_attrs else {}
        if selected:
            option_attrs.update(self.checked_attribute)
        if 'id' in option_attrs:
            option_attrs['id'] = self.id_for_label(option_attrs['id'], index)

        if isinstance(value, str):
            label = '<div class="user-option"><div class="text-placeholder">Select user...</div></div>'
        else:
            instance = value.instance
            full_name = instance.wagtail_userprofile.profile.full_name
            username = instance.username
            image = instance.wagtail_userprofile.profile.profile_image
            avatar = AVATAR.format(image) if image else PLACEHOLDER
            label = f'<div class="user-option">{avatar}<div class="user-label">{full_name} <span>{username}</span></div></div>'
            if self.handle_form_fields:
                self.option_data[instance.id] = {
                    'name': full_name,
                    'username': username,
                    'avatar': image,
                }

        return {
            'name': name,
            'value': value,
            'label': label,
            'selected': selected,
            'index': index,
            'attrs': option_attrs,
            'type': self.input_type,
            'template_name': self.option_template_name,
            'wrap_label': True,
        }

    def build_attrs(self, *args, **kwargs):
        attrs = super().build_attrs(*args, **kwargs)
        attrs['data-controller'] = 'userselect'
        attrs['data-user-select'] = True
        if self.handle_form_fields:
            attrs['data-handle-form-fields'] = True
            attrs['data-options'] = json.dumps(self.option_data)
        return attrs

    @property
    def media(self):
        return Media(
            js=['js/user-select-controller.js'],
            css={'all': ['css/user-select-widget.css']},
        )
