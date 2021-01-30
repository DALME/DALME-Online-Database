
from dalme_app.models import Place
from ._common import DynamicSerializer


class PlaceSerializer(DynamicSerializer):

    class Meta:
        model = Place
        fields = ('id', 'standard_name', 'notes', 'locale')
        extra_kwargs = {
            'notes': {'required': False},
            'locale': {'required': False},
        }

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if ret['locale']:
            ret['locale'] = {
                'id': instance.locale.id,
                'name': instance.locale.name,
                'administrative_region': instance.locale.administrative_region,
                'country': instance.locale.country.name
            }
        return ret

    def to_internal_value(self, data):
        if data.get('locale', {}).get('id') is not None:
            print(data['locale']['id'])
            data['locale'] = data['locale']['id']
        return super().to_internal_value(data)
