"""Serializer for UI options."""

from rest_framework import serializers


class OptionsSerializer(serializers.Serializer):
    label = serializers.ReadOnlyField()
    value = serializers.SerializerMethodField()
    group = serializers.ReadOnlyField(required=False)
    detail = serializers.ReadOnlyField(required=False)
    icon = serializers.ReadOnlyField(required=False)

    class Meta:
        fields = [
            'label',
            'value',
            'group',
            'detail',
            'icon',
        ]

    def __init__(self, *args, **kwargs):
        self.concordance = kwargs.pop('concordance', None)
        self.model_name = kwargs.pop('model_name', None)
        super().__init__(*args, **kwargs)

    def get_value(self, obj):
        """Ensure that number values are returned as int."""
        if isinstance(obj['value'], str):
            value = obj['value']
            return int(value) if value.isdigit() else value
        return obj

    def get_fields(self):
        """Alter fields based on concordance."""
        fields = super().get_fields()
        if self.concordance:
            for key, value in self.concordance.items():
                fields[key] = serializers.ReadOnlyField(source=value, required=False)
        if self.model_name:
            fields['model'] = serializers.ReadOnlyField(default=self.model_name, required=False)

        return fields
