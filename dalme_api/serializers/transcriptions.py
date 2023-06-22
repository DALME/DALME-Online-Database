from rest_framework import serializers

from dalme_app.models import Transcription


class TranscriptionSerializer(serializers.ModelSerializer):
    """Serializer for transcriptions."""

    author = serializers.CharField(max_length=255, required=False)

    class Meta:  # noqa: D106
        model = Transcription
        fields = ('id', 'transcription', 'author', 'version')
