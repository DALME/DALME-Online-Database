from dalme_app.models import Content_type
from rest_framework import serializers
from ._common import DynamicSerializer
import dalme_app.serializers.others as _others


class ContentTypeSerializer(DynamicSerializer):
    cont_class = serializers.StringRelatedField(source='content_class', required=False)
    attribute_types = _others.AttributeTypeSerializer(many=True, required=False)

    class Meta:
        model = Content_type
        fields = ('id', 'name', 'short_name', 'content_class', 'cont_class', 'description', 'attribute_types', 'has_pages', 'parents', 'has_inventory', 'r1_inheritance', 'r2_inheritance')
        extra_kwargs = {'name': {'validators': []}}

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if ret.get('content_class') is not None and ret.get('cont_class') is not None:
            name = ret.pop('cont_class')
            ret['content_class'] = {'name': name, 'value': ret['content_class']}
        if ret.get('parents') is not None:
            ctype_dict = {i.id: i.name for i in Content_type.objects.all()}
            list_ids = ret['parents'].split(',') if ',' in ret['parents'] else [ret['parents']]
            ret['parents'] = [{'id': int(i), 'name': ctype_dict[int(i)]} for i in list_ids]
        return ret
