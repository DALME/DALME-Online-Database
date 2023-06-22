from rest_framework import serializers

from dalme_app.models import Attribute, Collection, CollectionMembership, Record
from dalme_app.utils import DalmeDate


class PublicAttributeSerializer(serializers.ModelSerializer):
    """Record attribute serializer for web frontend."""

    class Meta:  # noqa: D106
        model = Attribute
        fields = ('name', 'value')

    def to_representation(self, instance):
        """Transform outgoing data."""
        # label = instance.attribute_type.short_name
        # if instance.attribute_type.data_type == 'TXT':
        #     return {label: instance.value_TXT}
        # else:
        #     return {label: str(instance)}
        return {instance.name: str(instance.value)}


class PublicFilteredCollectionsSerializer(serializers.ListSerializer):
    """Filtered collection serializer for web frontend."""

    def to_representation(self, data):
        """Transform outgoing data."""
        data = data.filter(collection_id__is_published=True)
        return super().to_representation(data)


class PublicCollectionMembershipSerializer(serializers.ModelSerializer):
    """Serializes record membership in collections for web frontend."""

    name = serializers.CharField(source='collection_id.name', read_only=True, required=False, max_length=255)

    class Meta:  # noqa: D106
        list_serializer_class = PublicFilteredCollectionsSerializer
        model = CollectionMembership
        fields = ('collection_id', 'name')


class PublicRecordSerializer(serializers.ModelSerializer):
    """Records serializer for web frontend."""

    name = serializers.CharField(max_length=255)
    short_name = serializers.CharField(max_length=55, required=True)
    parent = serializers.PrimaryKeyRelatedField(queryset=Record.objects.all(), allow_null=True)
    parent_name = serializers.StringRelatedField(source='parent', read_only=True, required=False)
    no_folios = serializers.IntegerField(required=False)
    no_images = serializers.IntegerField(required=False)
    attributes = PublicAttributeSerializer(many=True, required=False)
    collections = PublicCollectionMembershipSerializer(many=True, required=False)

    class Meta:  # noqa: D106
        model = Record
        fields = (
            'id',
            'name',
            'short_name',
            'parent',
            'parent_name',
            'no_folios',
            'no_images',
            'no_transcriptions',
            'collections',
            'attributes',
            'has_images',
            'has_transcriptions',
            'get_credit_line',
        )

    def to_representation(self, instance):
        """Transform outgoing data."""
        ret = super().to_representation(instance)
        name_string = ret['name'].split('(')
        ret['image_ref'] = self.get_image(instance)

        try:
            ret['short_name'] = name_string[1][:-1]
        except IndexError:
            ret['short_name'] = 'N/A'

        ret['name'] = name_string[0]
        ret['archival_location'], ret['format_info'], ret['parent_type'] = self.get_archival_info(instance)
        attributes = ret.pop('attributes')
        if attributes is not None:
            for k, v in self.process_attributes(attributes).items():
                ret[k] = v
        return ret

    @staticmethod
    def get_image(instance):
        """Return image id from DAM."""
        page = instance.pages.exclude(dam_id__isnull=True).first()
        return page.dam_id if page else None

    @staticmethod
    def process_attributes(qset):
        """Reformat attributes."""
        result = {}
        dates = {}
        for i in qset:
            ((k, v),) = i.items()
            if k in ['start_date', 'end_date', 'date']:
                dates[k] = v
            else:
                result[k] = v
        if dates:
            if 'start_date' in dates and 'end_date' in dates:
                result['date'] = DalmeDate([dates['start_date'], dates['end_date']]).format_as('mys')
                result['full_date'] = DalmeDate([dates['start_date'], dates['end_date']]).format_as('dmyl')
            elif 'date' in dates:
                result['date'] = DalmeDate(dates['date']).format_as('mys')
                result['full_date'] = DalmeDate(dates['date']).format_as('dmyl')
            else:
                result['date'] = DalmeDate(list(dates.values())[0]).format_as('mys')
                result['full_date'] = DalmeDate(list(dates.values())[0]).format_as('dmyl')
        else:
            result['date'] = '—'
            result['full_date'] = 'N/A'
        return result

    def get_archival_info(self, instance):
        """Return provenance information."""
        _parent = instance.parent
        loc = _parent.name

        if hasattr(_parent, 'parent'):  # register
            try:
                format_values = {
                    i['attribute_type__short_name']: i['value'].lower()
                    for i in _parent.attributes.filter(
                        attribute_type__short_name__in=['support', 'format'],
                    ).values('attribute_type__short_name', 'value')
                }
                fmt = format_values.get('support')
                if format_values.get('format'):
                    fmt = fmt + f', {format_values["format"]}' if fmt else format_values.get('format')
            except:  # noqa: E722
                fmt = None

            archive_name = _parent.parent.name
            archive_url = _parent.parent.attributes.filter(attribute_type__short_name='url')
            archive_url = archive_url.first().value if archive_url.exists() else None
            marks = loc.replace(archive_name, '').strip() if archive_name in loc else None
            marks = marks[1:] if marks and marks.startswith(',') else marks
            if archive_name and archive_url and marks:
                return (f'<a href="{archive_url}" target="_blank">{archive_name}</a>, {marks}', fmt, 'register')
            return (loc, fmt, 'register')
        zotero_key = _parent.attributes.filter(attribute_type__short_name='zotero_key')
        zotero_key = zotero_key.first().value if zotero_key.exists() else None
        return (
            (
                f'<a href="/project/bibliography/#{zotero_key}">{loc}</a>',
                None,
                'edition',
            )
            if zotero_key
            else (loc, None, 'edition')
        )


class PublicCollectionSerializer(serializers.ModelSerializer):
    """Collections serializer for web frontend."""

    class Meta:  # noqa: D106
        model = Collection
        fields = '__all__'
