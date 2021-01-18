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
        ret['archival_location'], ret['format_info'], ret['parent_type'] = self.get_archival_info(instance)
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
                result['full_date'] = FormatDalmeDate([dates['start_date'], dates['end_date']]).format('long', 'full')
            elif 'date' in dates:
                result['date'] = FormatDalmeDate(dates['date']).format('short', 'month_year')
                result['full_date'] = FormatDalmeDate(dates['date']).format('long', 'full')
            else:
                result['date'] = FormatDalmeDate(list(dates.values())[0]).format('short', 'month_year')
                result['full_date'] = FormatDalmeDate(list(dates.values())[0]).format('long', 'full')
        else:
            result['date'] = '—'
            result['full_date'] = 'N/A'
        return result

    def get_archival_info(self, instance):
        _parent = instance.parent
        loc = _parent.name

        if _parent.parent:  # register
            try:
                format_values = {
                    i['attribute_type__short_name']: i['value_STR'].lower()
                    for i in _parent.attributes.filter(attribute_type__short_name__in=['support', 'format']).values('attribute_type__short_name', 'value_STR')
                    }
                format = format_values.get('support')
                if format_values.get('format'):
                    if format:
                        format += f', {format_values["format"]}'
                    else:
                        format = format_values.get('format')
            except: # noqa
                format = None
            archive_name = _parent.parent.name
            archive_url = _parent.parent.attributes.filter(attribute_type__short_name='url')
            archive_url = archive_url.first().value_STR if archive_url.exists() else None
            marks = loc.replace(archive_name, '').strip() if archive_name in loc else None
            marks = marks[1:] if marks and marks.startswith(',') else marks
            if archive_name and archive_url and marks:
                return (f'<a href="{archive_url}" target="_blank">{archive_name}</a>, {marks}', format, 'register')
            else:
                return (loc, format, 'register')
        else:  # edition
            zotero_key = _parent.attributes.filter(attribute_type__short_name='zotero_key')
            zotero_key = zotero_key.first().value_STR if zotero_key.exists() else None
            return (f'<a href="/project/bibliography/#{zotero_key}">{loc}</a>', None, 'edition') if zotero_key else (loc, None, 'edition')


class PublicCollectionSerializer(serializers.ModelSerializer):
    """ Collections serializer for web frontend """
    class Meta:
        model = Set
        fields = '__all__'
