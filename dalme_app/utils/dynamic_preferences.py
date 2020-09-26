import json
from django import forms
from dynamic_preferences.types import BasePreferenceType
from dynamic_preferences.serializers import BaseSerializer


class JSONPreferenceSerializer(BaseSerializer):
    """ Serializer for JSONPreference type. Extends django-dynamic-preferences BaseSerializer. """

    @classmethod
    def to_db(cls, value, **kwargs):
        try:
            if type(value) not in [dict, list] and value is not None and value != '':
                value = eval(value)
            return json.dumps(value)
        except ValueError:
            raise cls.exception("JSON incorrectly formatted.")

    @classmethod
    def to_python(cls, value, **kwargs):
        if not value:
            return ''
        try:
            return json.loads(value)
        except ValueError:
            raise cls.exception("Failed to deserialise value.")


class JSONPreference(BasePreferenceType):
    """ Preference type to store JSON serialized data.
    Extends django-dynamic-preferences BasePreferenceType. """

    widget = forms.Textarea
    field_class = forms.CharField
    serializer = JSONPreferenceSerializer
