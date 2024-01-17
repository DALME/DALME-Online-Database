"""Serializers for transcription data."""
from rest_framework import serializers

from ida.models import Transcription


class TranscriptionSerializer(serializers.ModelSerializer):
    """Serializer for transcriptions."""

    author = serializers.CharField(max_length=255, required=False)

    class Meta:
        model = Transcription
        fields = [
            'id',
            'transcription',
            'author',
            'version',
        ]
