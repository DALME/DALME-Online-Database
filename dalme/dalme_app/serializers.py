from dalme_app.models import (Attribute_type, Attribute, Attribute_DATE, Attribute_DBR, Attribute_INT,
Attribute_STR, Attribute_TXT, Content_class, Content_type, Content_type_x_attribute_type,
Content_list, Content_list_x_content_type, Source)
from rest_framework import serializers

class DynamicSerializer(serializers.Serializer):
    """
    A serializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

class SourceNameSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    url = serializers.CharField(max_length=255)

class SourceSerializer(DynamicSerializer):
    name = SourceNameSerializer()
    type = serializers.CharField(max_length=255)
    parent_source = serializers.CharField(max_length=255)
    is_inventory = serializers.BooleanField()
    url = serializers.CharField(max_length=255)
    mk2_identifier = serializers.CharField(max_length=255)
    mk1_identifier = serializers.CharField(max_length=255)
    alt_identifier = serializers.CharField(max_length=255)
    title = serializers.CharField(max_length=255)
    short_title = serializers.CharField(max_length=255)
    language = serializers.CharField(max_length=255)
    language_gc = serializers.CharField(max_length=255)
    archival_series = serializers.CharField(max_length=255)
    archival_number = serializers.CharField(max_length=255)
    start_date_day = serializers.CharField(max_length=255)
    start_date_month = serializers.CharField(max_length=255)
    start_date_year = serializers.CharField(max_length=255)
    end_date_day = serializers.CharField(max_length=255)
    end_date_month = serializers.CharField(max_length=255)
    end_date_year = serializers.CharField(max_length=255)
    end_date = serializers.CharField(max_length=255)
    start_date = serializers.CharField(max_length=255)
    dataset = serializers.CharField(max_length=255)
    act_type = serializers.CharField(max_length=255)
    act_type_phrase = serializers.CharField(max_length=255)
    debt_phrase = serializers.CharField(max_length=255)
    debt_amount = serializers.IntegerField()
    debt_unit = serializers.CharField(max_length=255)
    debt_unit_type = serializers.CharField(max_length=255)
    debt_source = serializers.CharField(max_length=255)
    comments = serializers.CharField()
    city = serializers.CharField(max_length=255)
