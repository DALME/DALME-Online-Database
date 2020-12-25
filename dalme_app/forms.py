from django import forms
from dynamic_preferences.forms import PreferenceForm
from dynamic_preferences.users.registries import user_preferences_registry
from dynamic_preferences.registries import global_preferences_registry
from collections import OrderedDict


class SearchForm(forms.Form):

    JOIN_TYPES = (
        ('must', 'AND'),
        ('must_not', 'NOT'),
        ('should', 'OR'),
    )

    QUERY_TYPES = (
        ('match_phrase', 'the following word(s)'),
        ('match', 'word(s) similar to'),
        ('prefix', 'word(s) beginning with'),
        ('term', 'exactly this expression')
    )

    RANGE_TYPES = (
        ('value', 'exactly'),
        ('lt', 'before'),
        ('gt', 'after'),
    )

    join_type = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={'class': 'form-control form-control-sm form-operator'}),
        choices=JOIN_TYPES,
        help_text='<p class=&quot;text-left p-1&quot;>\
                    <b>AND:</b> both the current and previous clauses must match<br/> \
                    <b>NOT:</b> the current clause must not match<br/> \
                    <b>OR:</b> either the current or previous clauses must match<br/></p>'
    )

    field = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'}),
        choices=[],
        help_text='Field to search'
    )

    field_type = forms.CharField(
        required=False,
        widget=forms.HiddenInput(),
        initial='text'
    )

    query_type = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'}),
        choices=QUERY_TYPES,
        help_text='<p class=&quot;text-left p-1&quot;>\
                    <b>Matches:</b> words must be present in field, but does not preserve their order<br/> \
                    <b>Contains:</b> query must be present within field, preserves word order<br/> \
                    <b>Begins with:</b> field must begin with word/phrase in query<br/> \
                    <b>Is:</b> field must exactly match query<br/><p>'
    )

    range_type = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'}),
        choices=RANGE_TYPES,
        help_text='<p class=&quot;text-left p-1&quot;> \
                    <b>Exactly:</b> matches the date in the query<br/> \
                    <b>Before:</b> matches any date before the date in the query<br/> \
                    <b>After with:</b> matches any date after the date in the query<br/></p>'
    )

    field_value = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'type': 'search',
                'placeholder': 'Type a query to search in record names',
                'autocomplete': 'off',
                'autocorrect': 'off',
                'autocapitalize': 'off',
                'spellcheck': 'false',
                'class': 'form-control form-control-sm'
            }
        ),
        help_text='Value to search'
    )

    query = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'type': 'search',
                'placeholder': 'Query',
                'autocomplete': 'off',
                'autocorrect': 'off',
                'autocapitalize': 'off',
                'spellcheck': 'false',
                'class': 'form-control form-control-sm'
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', [])
        super().__init__(*args, **kwargs)
        self.fields['field'].choices = fields


class GlobalPreferenceForm(PreferenceForm):
    registry = global_preferences_registry

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if self.fields[field].widget.__class__.__name__ == 'CheckboxInput':
                self.fields[field].widget.attrs.update({'class': 'form-check-input'})
            else:
                self.fields[field].widget.attrs.update({'class': 'form-control form-control-sm'})


class UserPreferenceForm(PreferenceForm):
    registry = user_preferences_registry

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if self.fields[field].widget.__class__.__name__ == 'CheckboxInput':
                self.fields[field].widget.attrs.update({'class': 'form-check-input'})
            else:
                self.fields[field].widget.attrs.update({'class': 'form-control form-control-sm'})


def preference_form_builder(form_base_class, **kwargs):
    registry = form_base_class.registry
    preferences_obj = registry.preferences()

    fields = OrderedDict()
    instances = []
    manager_kwargs = {"instance": kwargs.get("instance", None)}
    manager = registry.manager(**manager_kwargs)

    for preference in preferences_obj:
        f = preference.field
        instance = manager.get_db_pref(section=preference.section.name, name=preference.name)
        f.initial = instance.value
        f.section = preference.section.name
        fields[preference.identifier()] = f
        instances.append(instance)

    form_class = type('Custom' + form_base_class.__name__, (form_base_class,), {})
    form_class.base_fields = fields
    form_class.preferences = preferences_obj
    form_class.instances = instances
    form_class.manager = manager
    return form_class
