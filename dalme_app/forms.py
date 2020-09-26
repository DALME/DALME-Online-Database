from dynamic_preferences.forms import PreferenceForm
from dynamic_preferences.users.registries import user_preferences_registry
from dynamic_preferences.registries import global_preferences_registry
from collections import OrderedDict


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
