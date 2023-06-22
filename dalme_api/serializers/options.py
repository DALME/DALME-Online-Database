from rest_framework import serializers


class OptionsSerializer(serializers.Serializer):
    """Serializer for UI options."""

    label = serializers.CharField()
    value = serializers.CharField()
    group = serializers.CharField(required=False)
    detail = serializers.CharField(required=False)

    class Meta:  # noqa: D106
        fields = ['label', 'value', 'group', 'detail']

    def __init__(self, *args, **kwargs):  # noqa: D107
        self.concordance = kwargs.pop('concordance', None)
        super().__init__(*args, **kwargs)

    def get_fields(self):
        """Alter fields based on concordance."""
        fields = super().get_fields()
        if self.concordance:
            for key, value in self.concordance.items():
                fields[key] = serializers.CharField(source=value)
        return fields
