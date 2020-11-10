from dalme_app.models import LocaleReference
from rest_framework import serializers


class LocaleReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocaleReference
        fields = ('id', 'name', 'administrative_region', 'country', 'latitude', 'longitude')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if ret.get('country') is not None:
            ret['country'] = {
                'name': instance.country.name,
                'id': instance.country.id
                }
        return ret

    def to_internal_value(self, data):
        if data.get('country') is not None and type(data.get('country')) is dict:
            data['country'] = data['country']['id']
        return super().to_internal_value(data)
