from django.contrib.auth.models import User, Group
from dalme_app.models import *
from rest_framework import serializers
from dalme_app import functions
import uu, base64, ast
from datetime import datetime
from django.utils import timezone

class DynamicSerializer(serializers.ModelSerializer):
    """ A serializer that takes an additional `fields` argument that
    indicates which fields should be removed. """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        rem_fields = kwargs.pop('fields', None)
        # Instantiate the superclass normally
        super(DynamicSerializer, self).__init__(*args, **kwargs)
        if rem_fields is not None:
            for field_name in rem_fields:
                self.fields.pop(field_name)

class FieldAttributesSerializer(serializers.ModelSerializer):
    field = serializers.StringRelatedField()

    class Meta:
        model = DT_fields
        fields = '__all__'

class ListsSerializer(DynamicSerializer):
    class Meta:
        model = DT_list
        fields = '__all__'

class WorksetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workset
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class TaskListSerializer(serializers.ModelSerializer):
    task_count = serializers.IntegerField()

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['group'] = Group.objects.get(pk=ret['group']).name
        task_count = ret.pop('task_count')
        ret['name'] = '<div class="d-flex"><div class="align-self-start mr-auto">'+ret['name']+'</div><div class="badge badge-primary badge-pill align-self-end">'+str(task_count)+'</div></div>'
        return ret

    class Meta:
        model = TaskList
        fields = ('id', 'name', 'group', 'task_count')

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
        ret['id'] = ret['ref']
        ret['ref'] = {'ref': ret['ref'], 'url': '/images/'+str(ret['ref'])}
        return ret

    class Meta:
        model = rs_resource
        fields = ('ref', 'has_image','creation_date','created_by','field12','field8','field3','field51','field79','collections')

class TranscriptionSerializer(serializers.ModelSerializer):
    """ Basic serializer for transcriptions """
    author = serializers.CharField(max_length=255, required=False)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if ret['transcription']:
            transcription_xml = '<xml>'+ret['transcription']+'</xml>'
            ret['transcription_html'] = functions.render_transcription(transcription_xml)
        else:
            ret['transcription_html'] = ''
        return ret

    class Meta:
        model = Transcription
        fields = ('id', 'transcription', 'author', 'version')

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
        extra_kwargs = {
            'username': {
                'validators': [],
            }
        }

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

    def update(self, instance, validated_data):
        """ Update profile and user. Assumes there is a user for every profile """
        user_data = validated_data.pop('user')
        super().update(instance, validated_data)
        user = instance.user
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()
        groups = self.context['groups']
        user.groups.clear()
        for g in groups:
            user.groups.add(g)
        return instance

    def create(self, validated_data):
        """ Create profile and user. Assumes there is a user for every profile """
        user_data = validated_data.pop('user')
        user_data.pop('groups')
        groups = self.context['groups']
        user = User.objects.create_user(**user_data)
        for g in groups:
            user.groups.add(g)
        profile = Profile.objects.create(user=user, **validated_data)
        return profile

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
