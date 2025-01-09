"""Serializer for UI options."""

from rest_framework import serializers


class OptionsSerializer(serializers.Serializer):
    label = serializers.ReadOnlyField()
    value = serializers.ReadOnlyField()
    group = serializers.ReadOnlyField(required=False)
    detail = serializers.ReadOnlyField(required=False)

    class Meta:
        fields = [
            'label',
            'value',
            'group',
            'detail',
        ]

    def __init__(self, *args, **kwargs):
        self.concordance = kwargs.pop('concordance', None)
        super().__init__(*args, **kwargs)

    def get_fields(self):
        """Alter fields based on concordance."""
        fields = super().get_fields()
        if self.concordance:
            for key, value in self.concordance.items():
                fields[key] = serializers.ReadOnlyField(source=value)
        return fields
