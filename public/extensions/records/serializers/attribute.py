"""Serializer for attributes."""

from rest_framework import serializers

from ida.models import Attribute


class AttributeSerializer(serializers.ModelSerializer):
    """Record attribute serializer for web frontend."""

    class Meta:
        model = Attribute
        fields = [
            'name',
            'value',
        ]

    def to_representation(self, instance):
        """Transform outgoing data."""
        return {instance.name: str(instance.value)}
