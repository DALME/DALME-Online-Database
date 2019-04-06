from django.contrib.auth.models import User
from dalme_app.models import *
from rest_framework import serializers
from dalme_app import functions

class DynamicSerializer(serializers.ModelSerializer):
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

class PageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Page
        fields = ('name', 'dam_id','order')


class ImageSerializer(serializers.ModelSerializer):
    collections = serializers.CharField(max_length=255)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        try:
            ret['created_by'] = rs_user.objects.get(ref=ret['created_by']).username
        except:
            ret['created_by'] = ret['created_by']

        ret['ref'] = {'ref': ret['ref'], 'url': '/images/'+str(ret['ref'])}

        return ret

    class Meta:
        model = rs_resource
        fields = ('ref', 'has_image','creation_date','created_by','field12','field8','field3','field51','field79','collections')

class TranscriptionSerializer(serializers.ModelSerializer):
    """
    Basic serializer for transcriptions
    """
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        transcription_xml = '<xml>'+ret['transcription']+'</xml>'
        ret['transcription_html'] = functions.render_transcription(transcription_xml)
        return ret

    class Meta:
        model = Transcription
        fields = '__all__'

class AttributeSerializer(serializers.ModelSerializer):
    """
    Basic serializer for attribute data
    """

    def to_representation(self, instance):
        types = Attribute_type.objects.all()
        type_dict = {}
        for t in types:
            type_dict[t.id] = [t.short_name,t.data_type]

        ret = super().to_representation(instance)
        new_ret = {}
        for i in ret:
            dtype = type_dict[ret['attribute_type']][1]
            label = type_dict[ret['attribute_type']][0]
            if dtype == 'DATE':
                value = ret['value_STR']
            else:
                value = eval("ret['value_"+ dtype +"']")

            new_ret[label] = value

        return new_ret

    class Meta:
        model = Attribute
        fields = ('attribute_type', 'value_STR', 'value_TXT', 'value_INT', 'value_DBR')

class SourceSerializer(DynamicSerializer):
    type = serializers.StringRelatedField()
    name = serializers.CharField(max_length=255)
    parent_source_id = serializers.PrimaryKeyRelatedField(source='parent_source', read_only=True)
    parent_source = serializers.StringRelatedField()
    attributes = AttributeSerializer(many=True)
    no_folios = serializers.IntegerField()

    def to_representation(self, instance):
        """Create dictionaries for fields with links"""
        fields = self.context.get('fields')
        ret = super().to_representation(instance)

        attributes = ret.pop('attributes')
        for i in attributes:
            (k, v), = i.items()
            ret[k] = v

        ret['name'] = {'name': ret['name'], 'url': '/sources/'+ret['id']}
        ret['parent_source'] = {'name': ret['parent_source'], 'url': '/sources/'+str(ret['parent_source_id'])}
        if 'url' in ret:
            ret['url'] = {'name': 'Visit Link', 'url': ret['url']}

        return ret

    class Meta:
        model = Source
        fields = ('id','type','name','short_name','parent_source','parent_source_id','is_inventory', 'attributes', 'no_folios')

class UserSerializer(serializers.ModelSerializer):
    """
    Basic serializer for user data
    """
    class Meta:
        model = User
        fields = ('id','last_login','is_superuser','username','first_name','last_name','email','is_staff','is_active','date_joined')

class ProfileSerializer(serializers.ModelSerializer):
    """
    Serialises user profiles and combines user data
    """
    user = UserSerializer(required=True)

    class Meta:
        model = Profile
        fields = ('id','full_name','user_id','dam_usergroup','dam_userid','wiki_groups','wiki_userid','wiki_username','wp_userid','wp_role','wp_avatar_url', 'user')

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
        fields = ('id','code','level','type','text')

class ContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content_type
        fields = ('id', 'name', 'description', 'content_class', 'short_name')

class AttributeTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attribute_type
        fields = ('id', 'name', 'short_name', 'description', 'data_type')

class ContentClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content_class
        fields = ('id', 'name', 'short_name', 'description')

class ContentXAttributeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='attribute_type.id')
    name = serializers.CharField(max_length=255, source='attribute_type.name')
    short_name = serializers.CharField(max_length=55, source='attribute_type.short_name')
    description = serializers.CharField(source='attribute_type.description')
    data_type = serializers.CharField(max_length=15, source='attribute_type.data_type')

    class Meta:
        model = Content_attributes
        fields = '__all__'
