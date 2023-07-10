from rest_framework import serializers

from dalme_app.models import AttributeType


class AttributeTypeSerializer(serializers.ModelSerializer):
    """Serializer for attribute types."""

    class Meta:  # noqa: D106
        model = AttributeType
        fields = ('id', 'name', 'label', 'description', 'data_type', 'source', 'options', 'same_as')
