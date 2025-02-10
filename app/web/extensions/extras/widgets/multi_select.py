"""Multi-select widget."""

from django.forms import Media
from django.utils.functional import cached_property

from .custom_select import CustomSelect


class MultiSelect(CustomSelect):
    def __init__(  # noqa: PLR0913
        self,
        attrs=None,
        choices=(),
        placeholder='Click to select...',
        container_classes=None,
        multiselect=True,
        sortable=False,
        api_state=None,
        queryset=None,
    ):
        super().__init__(attrs, choices)
        self.placeholder = placeholder
        self.container_classes = container_classes if container_classes else []
        self.allow_multiple_selected = multiselect
        self.is_sortable = sortable
        self.use_api = api_state is not None
        self.queryset = queryset
        self.state_name = api_state
        self.option_list = []

    def format_label(self, value, label):  # noqa: ARG002
        """Format label function to be overriden by subclasses."""
        return label

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):  # noqa: PLR0913
        index = str(index) if subindex is None else '%s_%s' % (index, subindex)  # noqa: UP031
        option_attrs = self.build_attrs(self.attrs, attrs) if self.option_inherits_attrs else {}
        option_attrs = self.append_option_attrs(value, option_attrs)
        if selected:
            option_attrs.update(self.checked_attribute)
        if 'id' in option_attrs:
            option_attrs['id'] = self.id_for_label(option_attrs['id'], index)

        label = self.format_label(value, label)

        if not self.use_api:
            self.option_list.append({'id': value if isinstance(value, str) else value.instance.id, 'text': label})

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

    def append_option_attrs(self, value, option_attrs):  # noqa: ARG002
        """Append option attributes function to be overriden by subclasses."""
        return option_attrs

    def build_attrs(self, *args, **kwargs):
        attrs = super().build_attrs(*args, **kwargs)
        attrs['data-controller'] = 'multiselect'
        attrs['data-placeholder'] = self.placeholder
        attrs['data-use-api'] = self.use_api
        attrs['data-state-name'] = self.state_name if self.state_name else False

        if self.allow_multiple_selected:
            self.container_classes.append('select-multiple')
            attrs['multiple'] = 'multiple'
            attrs['data-sortable'] = self.is_sortable

        attrs['containerclasses'] = ' '.join(list(set(self.container_classes))) if self.container_classes else False

        return attrs

    @cached_property
    def media(self):
        return Media(
            js=['js/multi-select-controller.js'],
            css={'all': ['css/multi-select-widget.css']},
        )

    def value_from_datadict(self, data, files, name):
        value = super().value_from_datadict(data, files, name)
        if not value or (isinstance(value, list) and len(value) == 1 and value[0] == ''):
            return None
        if self.allow_multiple_selected and value and len(value) == 1 and ',' in value[0]:
            return [int(i) for i in value[0].split(',')]
        return value
