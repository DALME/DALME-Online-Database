"""Serializers for image data."""

from rest_framework import serializers

from domain.models.resourcespace import rs_collection, rs_resource


class RSCollectionsSerializer(serializers.ModelSerializer):
    """Serializer for RS/DAM collections."""

    class Meta:
        model = rs_collection
        fields = [
            'ref',
            'name',
            'user',
            'theme',
            'theme2',
            'theme3',
        ]

    def to_representation(self, instance):
        """Transform outgoing data."""
        ret = super().to_representation(instance)
        t_fields = [ret.pop(i) for i in ['theme', 'theme2', 'theme3']]
        ret['name'] = '≫'.join(t_fields)
        return ret


class RSImageSerializer(serializers.ModelSerializer):
    """Serializer for RS/DAM images."""

    class Meta:
        model = rs_resource
        fields = [
            'ref',
            'has_image',
            'creation_date',
            'created_by',
            'field12',
            'field8',
            'field3',
            'field51',
            'field79',
        ]


class ImageUrlSerializer(serializers.ModelSerializer):
    """Serializer for RS/DAM images with urls."""

    dam_id = serializers.IntegerField(source='ref')
    title = serializers.CharField(source='field8')

    class Meta:
        model = rs_resource
        fields = [
            'dam_id',
            'title',
        ]

    def to_representation(self, instance):
        """Transform outgoing data."""
        ret = super().to_representation(instance)
        ret.update({'url': instance.get_image_url()})
        return ret


class ImageOptionsSerializer(serializers.ModelSerializer):
    """Serializer for RS/DAM images as options."""

    dam_id = serializers.IntegerField(source='ref')
    title = serializers.CharField(source='field8')

    class Meta:
        model = rs_resource
        fields = [
            'dam_id',
            'title',
        ]
