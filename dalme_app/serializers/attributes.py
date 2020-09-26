from dalme_app.models import *
from rest_framework import serializers
import json


class AttributeSerializer(serializers.ModelSerializer):
    """ DT serializer for attribute data """

    class Meta:
        model = Attribute
        fields = ('attribute_type', 'value_STR', 'value_TXT', 'value_INT', 'value_DATE_d', 'value_DATE_m', 'value_DATE_y', 'value_JSON')

    def to_representation(self, instance):
        label = instance.attribute_type.short_name
        if instance.attribute_type.data_type in ['FK-UUID', 'FK-INT']:
            _id = '"{}"'.format(instance.value_JSON['id']) if instance.attribute_type.data_type == 'FK-UUID' else instance.value_JSON['id']
            object = eval('{}.objects.get(pk={})'.format(instance.value_JSON['class'], _id))
            return {label: {
                    'name': object.name,
                    'url': object.get_url(),
                    'id': json.dumps(instance.value_JSON)
                    }}
        elif instance.attribute_type.data_type == 'DATE':
            return {label: {
                'name': str(instance),
                'value': {
                    'd': instance.value_DATE_d,
                    'm': instance.value_DATE_m,
                    'y': instance.value_DATE_y
                }}}
        else:
            return {label: str(instance)}


class SimpleAttributeSerializer(serializers.ModelSerializer):
    """ Basic serializer for attribute data """
    attribute_name = serializers.StringRelatedField(source='attribute_type')
    attribute_type = serializers.PrimaryKeyRelatedField(read_only=True)
    data_type = serializers.CharField(max_length=15, source='attribute_type.data_type', read_only=True)
    options_list = serializers.CharField(max_length=15, source='attribute_type.options_list', read_only=True)

    class Meta:
        model = Attribute
        fields = ('id', 'attribute_type', 'value_STR', 'value_TXT', 'attribute_name',
                  'value_DATE_d', 'value_DATE_m', 'value_DATE_y', 'data_type', 'options_list')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.attribute_type.data_type != 'DATE':
            ret.pop('value_DATE_d')
            ret.pop('value_DATE_m')
            ret.pop('value_DATE_y')
        if instance.attribute_type.data_type != 'TXT':
            ret.pop('value_TXT')
        if instance.attribute_type.data_type != 'STR' and instance.attribute_type.data_type != 'INT' and instance.attribute_type.data_type != 'UUID':
            ret.pop('value_STR')
        return ret
