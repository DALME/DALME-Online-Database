"""Serializers for preferences data."""

from rest_framework import serializers

from domain.models import Preference


class PreferenceSerializer(serializers.ModelSerializer):
    """Serializer for preferences."""

    name = serializers.ReadOnlyField(source='key.name')
    label = serializers.ReadOnlyField(source='key.label')
    description = serializers.ReadOnlyField(source='key.description')
    data_type = serializers.ReadOnlyField(source='key.data_type')
    group = serializers.ReadOnlyField(source='key.group')
    default = serializers.ReadOnlyField(source='key.default')

    class Meta:
        model = Preference
        fields = [
            'name',
            'label',
            'description',
            'data_type',
            'group',
            'default',
            'value',
        ]
