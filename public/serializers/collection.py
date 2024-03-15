"""Serializer for collection."""

from rest_framework import serializers

from ida.models import Collection


class CollectionSerializer(serializers.ModelSerializer):
    """Collections serializer for web frontend."""

    class Meta:
        model = Collection
        fields = '__all__'
