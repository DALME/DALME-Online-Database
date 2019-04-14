from django.contrib.auth.models import User, Group
from dalme_app.models import *
from rest_framework import serializers
from dalme_app import functions
import uu, base64

class DynamicSerializer(serializers.ModelSerializer):
    """ A serializer that takes an additional `fields` argument that
    controls which fields should be displayed. """

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
    """ Basic serializer for transcriptions """
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        transcription_xml = '<xml>'+ret['transcription']+'</xml>'
        ret['transcription_html'] = functions.render_transcription(transcription_xml)
        return ret

    class Meta:
        model = Transcription
        fields = '__all__'

class AttributeSerializer(serializers.ModelSerializer):
    """ Basic serializer for attribute data """

    class Meta:
        model = Attribute
        fields = ('attribute_type', 'value_STR', 'value_TXT', 'value_INT', 'value_DBR')

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

class WikiGroupSerializer(serializers.ModelSerializer):
    """Basic serializer for user group data from the wiki database"""

    class Meta:
        model = wiki_user_groups
        fields = ('ug_group',)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        for key, value in ret.items():
            ret[key] = base64.b64decode(value).capitalize()
        return ret

    #def to_internal_value(self, data):
    #    """ convert string fields to binary representation + make lower case"""
    #    internal = super().to_internal_value(data)
    #    if internal['ug_group'] != None:
    #            internal['ug_group'] = base64.b64encode(internal['ug_group'].lower())
    #    return internal

class GroupSerializer(serializers.ModelSerializer):
    """ Basic serializer for user group data """
    name = serializers.CharField(max_length=255, required=False)
    class Meta:
        model = Group
        fields = ('id','name')

class UserSerializer(serializers.ModelSerializer):
    """ Basic serializer for user data """
    groups = GroupSerializer(many=True, required=False)

    class Meta:
        model = User
        fields = ('id','last_login','is_superuser','username','first_name','last_name','email','is_staff','is_active','date_joined','groups')

class ProfileSerializer(serializers.ModelSerializer):
    """ Serialises user profiles and combines user data """
    user = UserSerializer(required=True)
    dam_usergroup = serializers.ChoiceField(choices=rs_user.DAM_USERGROUPS, source='get_dam_usergroup', required=False)
    wiki_groups = serializers.SerializerMethodField(required=False)
    wp_role_display = serializers.ChoiceField(choices=Profile.WP_ROLE, source='get_wp_role_display', required=False)
    dam_usergroup_display = serializers.ChoiceField(choices=rs_user.DAM_USERGROUPS, source='get_dam_usergroup_display', required=False)

    class Meta:
        model = Profile
        fields = ('id','full_name','user_id','dam_usergroup','wiki_groups', 'wp_role', 'user', 'wp_role_display', 'dam_usergroup_display', 'wiki_user', 'dam_user', 'wp_user')

    def get_wiki_groups(self, obj):
        wg = wiki_user_groups.objects.filter(ug_user=obj.wiki_user)
        serializer = WikiGroupSerializer(instance=wg, many=True)
        return serializer.data

    def to_representation(self, instance):
        """ set display for choice fields """
        ret = super().to_representation(instance)
        if 'wp_role' in ret:
            if ret['wp_role'] != '':
                wp_role_d = ret.pop('wp_role_display')
                ret['wp_role'] = {'name': wp_role_d, 'value': ret['wp_role']}
        if 'dam_usergroup' in ret:
            if ret['dam_usergroup'] != '':
                dam_group_d = ret.pop('dam_usergroup_display')
                ret['dam_usergroup'] = {'name': dam_group_d, 'value': ret['dam_usergroup']}
        return ret

    def to_internal_value(self, data):
        """ revert display fields """
        if 'wp_role' in data:
            wp_role = data.pop('wp_role')['value']
            data['wp_role'] = wp_role
        if 'dam_usergroup' in data:
            dam_usergroup = data.pop('dam_usergroup')['value']
            data['dam_usergroup'] = dam_usergroup
        return super().to_internal_value(data)

    def update(self, instance, validated_data):
        """ Update profile and user. Assumes there is a user for every profile """
        user_data = validated_data.pop('user')
        super().update(instance, validated_data)
        user = instance.user
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()
        return instance

    def create(self, validated_data):
        """ Create profile and user. Assumes there is a user for every profile """
        user_data = validated_data.pop('user')
        groups = self.context['groups']
        user = User.objects.create_user(**user_data)
        for g in groups:
            #group = Group.objects.get(pk=g['id'])
            user.groups.add(g)
        profile = Profile.objects.create(user=user, **validated_data)
        return profile

class NotificationSerializer(serializers.ModelSerializer):
    code = serializers.IntegerField()

    class Meta:
        model = Notification
        fields = ('id','code','level','type','text')

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
