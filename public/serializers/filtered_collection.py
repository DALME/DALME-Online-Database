"""Serializer for filtered collections."""

from rest_framework import serializers


class FilteredCollectionsSerializer(serializers.ListSerializer):
    """Filtered collection serializer for web frontend."""

    def to_representation(self, data):
        """Transform outgoing data."""
        data = data.filter(collection_id__is_published=True)
        return super().to_representation(data)
