from rest_framework import serializers

from dalme_app.models import Source


class SourceOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ['id', 'name']
