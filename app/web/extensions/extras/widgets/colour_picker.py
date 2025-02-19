"""Colour picker widget."""

import json

from django.forms import Media, TextInput


class ColourPickerWidget(TextInput):
    def __init__(self, attrs=None, swatches=[], theme='default'):  # noqa: B006
        self.swatches = swatches
        self.theme = theme
        super().__init__(attrs=attrs)

    def build_attrs(self, *args, **kwargs):
        attrs = super().build_attrs(*args, **kwargs)
        attrs['data-controller'] = 'color'
        attrs['data-theme-value'] = self.theme
        attrs['data-color-swatches-value'] = json.dumps(self.swatches)
        return attrs

    @property
    def media(self):
        return Media(
            js=[
                'https://cdn.jsdelivr.net/gh/mdbassit/Coloris@latest/dist/coloris.min.js',
                'js/colour-picker-controller.js',
            ],
            css={'all': ['https://cdn.jsdelivr.net/gh/mdbassit/Coloris@latest/dist/coloris.min.css']},
        )
