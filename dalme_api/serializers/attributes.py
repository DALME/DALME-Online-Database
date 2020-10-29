from dalme_app.models import * # NOQA
from rest_framework import serializers
import json


class AttributeSerializer(serializers.ModelSerializer):
    """ DT serializer for attribute data """

    class Meta:
        model = Attribute # NOQA
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
        elif instance.attribute_type.data_type == 'TXT':
            return {label: instance.value_TXT}
        else:
            return {label: str(instance)}

    def to_internal_value(self, data):
        (key, value), = data.items()
        _type = Attribute_type.objects.get(short_name=key) # NOQA

        if _type.data_type == 'INT':
            data = {
                'attribute_type': _type.id,
                'value_INT': int(value)
            } if value is not None else None

        elif _type.data_type == 'TXT':
            data = {
                'attribute_type': _type.id,
                'value_TXT': value
            } if value is not None else None

        elif _type.data_type == 'DATE':
            value_dict = {}
            for item in ['d', 'm', 'y']:
                if value['value'].get(item) is not None:
                    value_dict['value_DATE_' + item] = value['value'][item]
            if value_dict:
                value_dict['attribute_type'] = _type.id
                data = value_dict
            else:
                data = None

        elif _type.data_type == 'FK-INT' or _type.data_type == 'FK-UUID':
            data = {
                'attribute_type': _type.id,
                'value_JSON': json.loads(value['id'])
            } if type(value) is dict and value.get('id') is not None else None

        elif _type.data_type == 'STR':
            data = {
                'attribute_type': _type.id,
                'value_STR': value
            } if value is not None else None

        return super().to_internal_value(data)


class SimpleAttributeSerializer(serializers.ModelSerializer):
    """ Basic serializer for attribute data """
    attribute_name = serializers.StringRelatedField(source='attribute_type')
    attribute_type = serializers.PrimaryKeyRelatedField(read_only=True)
    data_type = serializers.CharField(max_length=15, source='attribute_type.data_type', read_only=True)
    options_list = serializers.CharField(max_length=15, source='attribute_type.options_list', read_only=True)

    class Meta:
        model = Attribute # NOQA
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
