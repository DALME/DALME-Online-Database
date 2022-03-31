from django.contrib.auth.models import User

from rest_framework import serializers

from dalme_app.models import rs_resource as Resource
from dalme_api.serializers.users import UserSerializer


class ImageUrlSerializer(serializers.ModelSerializer):
    dam_id = serializers.IntegerField(source='ref')
    title = serializers.CharField(source='field8')

    class Meta:
        model = Resource
        fields = ['dam_id', 'title']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret.update({'url': instance.get_image_url()})
        return ret


class ImageOptionsSerializer(serializers.ModelSerializer):
    dam_id = serializers.IntegerField(source='ref')
    title = serializers.CharField(source='field8')

    class Meta:
        model = Resource
        fields = ['dam_id', 'title']