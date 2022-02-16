from rest_framework import serializers

from dalme_app.models import Attribute


class AttributeOptionsSerializer(serializers.Serializer):
    label = serializers.CharField()
    value = serializers.CharField()
    caption = serializers.CharField(required=False)

    class Meta:
        model = Attribute
        fields = ['caption', 'label', 'value']
