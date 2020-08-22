from dalme_app.models import (Source, Attribute, Set, Set_x_content)
from rest_framework import serializers
from dalme_app import functions
import json
import random


class AttributeSerializer(serializers.ModelSerializer):
    """ Record attribute serializer for web frontend """

    class Meta:
        model = Attribute
        fields = ('attribute_type', 'value_STR', 'value_TXT', 'value_INT')

    def to_representation(self, instance):
        label = instance.attribute_type.short_name
        if label == 'language':
            label = label + '_' + str(random.randint(0, 99))
        if instance.attribute_type.data_type == 'UUID':
            data = json.loads(instance.value_STR)
            object = eval('{}.objects.get(pk="{}")'.format(data['class'], data['id']))
            value = {
                'name': object.name,
                'url': object.get_url(),
                'value': instance.value_STR
            }
        else:
            value = str(instance)
        ret = {label: value}
        return ret


class FilteredSetsSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        data = data.filter(set_id__set_type='2')
        return super(FilteredSetsSerializer, self).to_representation(data)


class CollectionMembershipSerializer(serializers.ModelSerializer):
    """ Serializes record membership in collections for web frontend """
    name = serializers.CharField(source='set_id.name', read_only=True, required=False, max_length=255)
    # set_type = serializers.ChoiceField(choices=Set.SET_TYPES, source='set_id.get_set_type_display', required=False)

    class Meta:
        list_serializer_class = FilteredSetsSerializer
        model = Set_x_content
        fields = ('set_id', 'name')


class RecordSerializer(serializers.ModelSerializer):
    """ Records serializer for web frontend """
    type = serializers.StringRelatedField(read_only=True, required=False)
    # type = serializers.PrimaryKeyRelatedField(queryset=Content_type.objects.all())
    name = serializers.CharField(max_length=255)
    short_name = serializers.CharField(max_length=55, required=True)
    parent = serializers.PrimaryKeyRelatedField(queryset=Source.objects.all(), allow_null=True)
    parent_name = serializers.StringRelatedField(source='parent', read_only=True, required=False)
    no_folios = serializers.IntegerField(required=False)
    no_images = serializers.IntegerField(required=False)
    attributes = AttributeSerializer(many=True, required=False)
    inherited = AttributeSerializer(many=True, required=False)
    collections = CollectionMembershipSerializer(source='sets', many=True, required=False)

    class Meta:
        model = Source
        fields = ('id', 'type', 'name', 'short_name', 'is_public', 'parent', 'parent_name', 'no_folios', 'no_images', 'no_transcriptions', 'collections',
                  'attributes', 'inherited', 'has_images', 'has_transcriptions', 'get_credit_line')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        attributes = ret.pop('attributes')
        inherited = ret.pop('inherited')
        if attributes is not None:
            for k, v in self.process_attributes(attributes).items():
                ret[k] = v
        if inherited is not None:
            for k, v in self.process_attributes(inherited).items():
                ret[k] = v
        return ret

    def process_attributes(self, qset):
        result = {}
        dates = {}
        for i in qset:
            (k, v), = i.items()
            if k == 'start_date' or k == 'end_date':
                dates[k] = v
            else:
                result[k] = v
        if dates:
            if 'start_date' in dates:
                if 'end_date' in dates:
                    result['date'] = functions.get_date_range(dates['start_date'], dates['end_date'])
                else:
                    result['date'] = dates['start_date']
            else:
                result['date'] = dates['end_date']
        return result


class CollectionSerializer(serializers.ModelSerializer):
    """ Collections serializer for web frontend """
    class Meta:
        model = Set
        fields = '__all__'
