from django.contrib.auth.models import User
from dalme_app.models import (Attribute_type, Attribute, Attribute_DATE, Attribute_DBR, Attribute_INT,
Attribute_STR, Attribute_TXT, Content_class, Content_type, Content_type_x_attribute_type,
Content_list, Content_list_x_content_type, Source, Notification, Profile)
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

class SourceSerializer(DynamicSerializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
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

    def to_representation(self, instance):
        """Create dictionaries for fields with links"""
        ret = super().to_representation(instance)
        ret['name'] = {'name': ret['name'], 'url': '/source/'+ret['id']}
        if 'url' in ret:
            ret['url'] = {'name': 'Visit Link', 'url': ret['url']}
        return ret

class SourceSerializerTr(DynamicSerializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
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
    transcription = serializers.CharField()

class UserSerializer(serializers.ModelSerializer):
    """
    Basic serializer for user data
    """
    class Meta:
        model = User
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    """
    Serialises user profiles and combines user data
    """
    user = UserSerializer(required=True)

    class Meta:
        model = Profile
        fields = '__all__'

    def to_representation(self, instance):
        """
        Move fields from user to profile representation.
        """
        ret = super().to_representation(instance)
        user_representation = ret.pop('user')
        for key in user_representation:
            ret[key] = user_representation[key]

        if 'email' in ret:
            ret['email'] = {'name': ret['email'], 'url': 'mailto:'+ret['email']}

        return ret

    def to_internal_value(self, data):
        """
        Move fields related to user to their own user dictionary.
        """
        user_internal = {}
        for key in UserSerializer.Meta.fields:
            if key in data:
                user_internal[key] = data.pop(key)

        internal = super().to_internal_value(data)
        internal['user'] = user_internal
        return internal

    def update(self, instance, validated_data):
        """
        Update profile and user. Assumes there is a user for every profile.
        """
        user_data = validated_data.pop('user')
        super().update(instance, validated_data)

        user = instance.user
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()

        return instance

class NotificationSerializer(serializers.ModelSerializer):
    #level = serializers.ChoiceField(choices=Notification.LEVELS, source='get_level_display')
    #type = serializers.ChoiceField(choices=Notification.TYPES, source='get_type_display')
    #level = serializers.SerializerMethodField()
    #type = serializers.SerializerMethodField()
    code = serializers.IntegerField()

    def to_representation(self, instance):
        """Create dictionaries for fields with choices"""
        ret = super().to_representation(instance)
        ret['level'] = {'value': ret['level'], 'display': self.get_choice(ret['level'], 'LEVELS')}
        ret['type'] = {'value': ret['type'], 'display': self.get_choice(ret['type'], 'TYPES')}
        return ret

    def get_choice(self, obj, listname):
        if listname == 'LEVELS':
            list = Notification.LEVELS
        elif listname == 'TYPES':
            list = Notification.TYPES
        for t in list:
            if obj in t:
                label = t[1]
        return label

    class Meta:
        model = Notification
        fields = '__all__'

class ContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content_type
        fields = ('id', 'name', 'description', 'content_class', 'short_name')

class AttributeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute_type
        fields = '__all__'

class ContentClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content_class
        fields = '__all__'

class ContentXAttributeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='attribute_type.id')
    name = serializers.CharField(max_length=255, source='attribute_type.name')
    short_name = serializers.CharField(max_length=55, source='attribute_type.short_name')
    description = serializers.CharField(source='attribute_type.description')
    data_type = serializers.CharField(max_length=15, source='attribute_type.data_type')

    class Meta:
        model = Content_type_x_attribute_type
        fields = '__all__'
