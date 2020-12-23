from dalme_app.models import (Source, Attribute, Set, Set_x_content)
from rest_framework import serializers
from dalme_app.utils import FormatDalmeDate


class PublicAttributeSerializer(serializers.ModelSerializer):
    """ Record attribute serializer for web frontend """

    class Meta:
        model = Attribute
        fields = ('attribute_type', 'value_STR', 'value_TXT', 'value_INT')

    def to_representation(self, instance):
        label = instance.attribute_type.short_name
        if instance.attribute_type.data_type == 'TXT':
            return {label: instance.value_TXT}
        else:
            return {label: str(instance)}


class PublicFilteredSetsSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        data = data.filter(set_id__set_type='2')
        return super(PublicFilteredSetsSerializer, self).to_representation(data)


class PublicCollectionMembershipSerializer(serializers.ModelSerializer):
    """ Serializes record membership in collections for web frontend """
    name = serializers.CharField(source='set_id.name', read_only=True, required=False, max_length=255)
    # set_type = serializers.ChoiceField(choices=Set.SET_TYPES, source='set_id.get_set_type_display', required=False)

    class Meta:
        list_serializer_class = PublicFilteredSetsSerializer
        model = Set_x_content
        fields = ('set_id', 'name')


class PublicSourceSerializer(serializers.ModelSerializer):
    """ Records serializer for web frontend """
    type = serializers.StringRelatedField(read_only=True, required=False)
    # type = serializers.PrimaryKeyRelatedField(queryset=Content_type.objects.all())
    name = serializers.CharField(max_length=255)
    short_name = serializers.CharField(max_length=55, required=True)
    parent = serializers.PrimaryKeyRelatedField(queryset=Source.objects.all(), allow_null=True)
    parent_name = serializers.StringRelatedField(source='parent', read_only=True, required=False)
    no_folios = serializers.IntegerField(required=False)
    no_images = serializers.IntegerField(required=False)
    attributes = PublicAttributeSerializer(many=True, required=False)
    inherited = PublicAttributeSerializer(many=True, required=False)
    collections = PublicCollectionMembershipSerializer(source='sets', many=True, required=False)

    class Meta:
        model = Source
        fields = ('id', 'type', 'name', 'short_name', 'is_public', 'parent', 'parent_name', 'no_folios', 'no_images', 'no_transcriptions', 'collections',
                  'attributes', 'inherited', 'has_images', 'has_transcriptions', 'get_credit_line')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        name_string = ret['name'].split('(')
        try:
            ret['short_name'] = name_string[1][:-1]
        except IndexError:
            ret['short_name'] = 'N/A'
        ret['name'] = name_string[0]
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
            if k in ['start_date', 'end_date', 'date']:
                dates[k] = v
            else:
                result[k] = v
        if dates:
            if 'start_date' in dates and 'end_date' in dates:
                result['date'] = FormatDalmeDate([dates['start_date'], dates['end_date']]).format('short', 'month_year')
            elif 'date' in dates:
                result['date'] = FormatDalmeDate(dates['date']).format('short', 'month_year')
            else:
                result['date'] = FormatDalmeDate(list(dates.values())[0]).format('short', 'month_year')
        else:
            result['date'] = '—'
        return result


class PublicCollectionSerializer(serializers.ModelSerializer):
    """ Collections serializer for web frontend """
    class Meta:
        model = Set
        fields = '__all__'
