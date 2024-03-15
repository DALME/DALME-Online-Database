"""Serializer for collection membership."""

from rest_framework import serializers

from ida.models import CollectionMembership
from public.serializers.filtered_collection import FilteredCollectionsSerializer


class CollectionMembershipSerializer(serializers.ModelSerializer):
    """Serializes record membership in collections for web frontend."""

    name = serializers.CharField(source='collection_id.name', read_only=True, required=False, max_length=255)

    class Meta:
        list_serializer_class = FilteredCollectionsSerializer
        model = CollectionMembership
        fields = [
            'collection_id',
            'name',
        ]
