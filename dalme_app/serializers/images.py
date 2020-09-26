from dalme_app.models import rs_resource, rs_collection
from rest_framework import serializers


class RSCollectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = rs_collection
        fields = ('ref', 'name', 'user', 'theme', 'theme2', 'theme3')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        t_fields = [ret.pop(i) for i in ['theme', 'theme2', 'theme3']]
        ret['name'] = '≫'.join(t_fields)
        return ret


class RSImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = rs_resource
        fields = ('ref', 'has_image', 'creation_date', 'created_by', 'field12', 'field8',
                  'field3', 'field51', 'field79')
