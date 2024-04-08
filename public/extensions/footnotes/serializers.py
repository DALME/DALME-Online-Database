"""Footnote serializer."""

from rest_framework import serializers

from .models import Footnote


class FootnoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Footnote
        fields = ['id', 'page', 'text']
