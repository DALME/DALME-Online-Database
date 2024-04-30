"""Multi-select widget."""

from django.forms import Media, Select


class MultiSelect(Select):
    allow_multiple_selected = True

    def __init__(self, attrs=None, choices=(), placeholder='Click to select...'):
        super().__init__(attrs, choices)
        self.option_data = {}
        self.placeholder = placeholder

    def build_attrs(self, *args, **kwargs):
        attrs = super().build_attrs(*args, **kwargs)
        attrs['data-controller'] = 'multiselect'
        attrs['data-multiselect'] = True
        attrs['multiple'] = True
        if self.placeholder:
            attrs['data-placeholder'] = self.placeholder
        return attrs

    @property
    def media(self):
        return Media(
            js=['js/multi-select-controller.js'],
            css={'all': ['css/multi-select-widget.css']},
        )

    def value_from_datadict(self, data, files, name):
        value = super().value_from_datadict(data, files, name)
        if value and len(value) == 1 and ',' in value[0]:
            value = [int(i) for i in value[0].split(',')]
        return value
