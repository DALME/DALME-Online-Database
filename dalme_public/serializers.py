from dalme_app.models import (Source, Attribute, Set, Set_x_content)
from rest_framework import serializers
import json
import random


class PublicAttributeSerializer(serializers.ModelSerializer):
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
                    result['date'] = DALMEDateRange(dates['start_date'], dates['end_date']).long
                else:
                    result['date'] = dates['start_date']
            else:
                result['date'] = dates['end_date']
        return result


class PublicCollectionSerializer(serializers.ModelSerializer):
    """ Collections serializer for web frontend """
    class Meta:
        model = Set
        fields = '__all__'


class DALMEDateRange:
    ''' Class for managing date ranges throughout the app '''

    months_long = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
    months_short = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    months_int = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}

    def __init__(self, start_date, end_date):
        self.long = self.format_range(start_date, end_date, 'long')
        self.short = self.format_range(start_date, end_date, 'short')

    def format_range(self, start_date, end_date, format):
        if start_date == end_date:
            return self.format_date(start_date, format)
        else:
            start_date = self.get_date_elements(start_date, format)
            end_date = self.get_date_elements(end_date, format)
            if start_date[2] == end_date[2]:
                if start_date[1] == end_date[1] and start_date[1] is not None:
                    if start_date[0] is not None and end_date[0] is not None:
                        range_string = '{} to {} {}, {}' if format == 'long' else '{}-{}/{}/{}'
                        return range_string.format(str(start_date[0]), str(end_date[0]), start_date[1], start_date[2])
                    else:
                        return self.format_date(start_date, format)
                elif start_date[1] is not None and end_date[1] is not None:
                    if start_date[0] is not None and end_date[0] is not None:
                        range_string = '{} {} to {} {}, {}' if format == 'long' else '{}/{}-{}/{}/{}'
                        return range_string.format(str(start_date[0]), start_date[1], str(end_date[0]), end_date[1], start_date[2])
                    else:
                        range_string = '{} to {}, {}' if format == 'long' else '{}-{}/{}'
                        return range_string.format(start_date[1], end_date[1], start_date[2])
            else:
                if start_date[1] is not None and end_date[1] is not None:
                    if start_date[0] is not None and end_date[0] is not None:
                        range_string = '{} {}, {} to {} {}, {}' if format == 'long' else '{}/{}/{}-{}/{}/{}'
                        return range_string.format(str(start_date[0]), start_date[1], start_date[2], str(end_date[0]), end_date[1], end_date[2])
                    else:
                        range_string = '{} {} to {} {}' if format == 'long' else '{}/{}-{}/{}'
                        return range_string.format(start_date[1], start_date[2], end_date[1], end_date[2])
                else:
                    range_string = '{} to {}' if format == 'long' else '{}-{}'
                    return range_string.format(start_date[2], end_date[2])

    def get_day(self, date):
        return date[0] if len(date) == 3 else None

    def get_month(self, date, format):
        if len(date) > 1:
            if len(date[-2]) == 3:
                m_int = self.months_int[date[-2]]
            else:
                m_int = int(date[-2])
            return self.months_short[m_int] if format == 'short' else self.months_long[m_int]
        else:
            return None

    def get_year(self, date):
        return date[-1]

    def format_date(self, date, format):
        date = self.get_date_elements(date, format) if type(date) is not list else date
        if date[0] is not None:
            return '{} {}, {}'.format(str(date[0]), date[1], date[2]) if format == 'long' else '{}/{}/{}'.format(str(date[0]), date[1], date[2])
        elif date[1] is not None:
            return '{} {}'.format(date[1], date[2])
        else:
            return date[2]

    def get_date_elements(self, date, format):
        if '-' in str(date):
            date = str(date).split('-')
        else:
            date = [date]
        return [self.get_day(date), self.get_month(date, format), self.get_year(date)]
