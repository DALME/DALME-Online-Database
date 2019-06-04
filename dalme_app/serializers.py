from django.contrib.auth.models import User, Group
from dalme_app.models import (Profile, Content_class, Content_type, Content_attributes,
                              DT_list, DT_fields, Page, Source, Workset, TaskList, Task, wiki_user_groups,
                              rs_resource, Language, rs_collection, rs_user, Transcription, Attribute, Attribute_type,
                              Country, City, Tag)
from django_celery_results.models import TaskResult
from rest_framework import serializers
from dalme_app import functions
import base64


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


class DTFieldsSerializer(serializers.ModelSerializer):
    field_label = serializers.StringRelatedField(source='field')

    class Meta:
        model = DT_fields
        fields = ('id', 'list', 'field', 'render_exp', 'orderable', 'visible', 'searchable', 'dt_name', 'dte_name', 'dte_type',
                  'dte_options', 'dte_opts', 'dte_message', 'is_filter', 'filter_type', 'filter_options',
                  'filter_lookup', 'field_label', 'dt_class_name', 'dt_width', 'order')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if ret['field'] and ret['field_label']:
            name = ret.pop('field_label')
            ret['field'] = {'name': name, 'value': ret['field']}
        return ret


class DTListsSerializer(serializers.ModelSerializer):
    fields = DTFieldsSerializer(many=True, required=False)

    class Meta:
        model = DT_list
        fields = ('id', 'name', 'short_name', 'description', 'content_types', 'api_url', 'helpers', 'fields')
        extra_kwargs = {'content_types': {'required': False}}


class LanguageSerializer(serializers.ModelSerializer):
    parent_name = serializers.StringRelatedField(source='parent')

    class Meta:
        model = Language
        fields = ('id', 'glottocode', 'iso6393', 'name', 'type', 'parent', 'parent_name')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if ret['parent'] and ret['parent_name']:
            name = ret.pop('parent_name')
            ret['parent'] = {'name': name, 'value': ret['parent']}
        return ret


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('id', 'name', 'alpha_2_code', 'alpha_3_code', 'num_code')


class CitySerializer(serializers.ModelSerializer):
    country_name = serializers.StringRelatedField(source='country')

    class Meta:
        model = City
        fields = ('id', 'name', 'administrative_region', 'country', 'country_name')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        country_name = ret.pop('country_name')
        ret['country'] = {'name': country_name, 'value': ret['country']}
        return ret


class AsyncTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskResult
        fields = '__all__'


class WorksetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workset
        fields = ('id', 'name', 'description', 'owner', 'endpoint', 'progress')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['workset'] = '<div class="workset-title">{}</div><div class="workset-description">{}</div><div class="workset-endpoint">Endpoint: {}</div>'.format(ret['name'], ret['description'], ret['endpoint'])
        progress = ret['progress']
        angle = round((progress * 360 / 100))
        if angle <= 180:
            right_style = 'style="display:none;"'
            pie_style = ''
        else:
            right_style = 'style="transform:rotate(180deg);"'
            pie_style = 'style="clip:rect(auto, auto, auto, auto);"'
        left_style = 'style="transform:rotate(' + str(angle) + 'deg);"'
        progress_circle = '<div class="pie-wrapper"><span class="label">{}<span class="smaller">%</span></span><div class="pie" {}>'.format(round(progress), pie_style)
        progress_circle += '<div class="left-side half-circle" {}></div><div class="right-side half-circle" {}></div></div></div>'.format(left_style, right_style)
        ret['progress_circle'] = progress_circle
        return ret


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('title', 'task_list', 'due_date', 'completed', 'completed_date', 'created_by', 'assigned_to', 'description', 'workset', 'url', 'creation_timestamp', 'overdue_status')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['task'] = '<div class="task-title">{}</div><div class="task-description">{}</div>'.format(ret['title'], ret['description'])
        attachments = ''
        if ret['workset'] is not None:
            attachments += '<a href="/worksets/{}" class="task-attachment">Workset</a>'.format(ret['workset'])
        if ret['url'] is not None:
            attachments += '<a href="{}" class="task-attachment">URL</a>'.format(ret['url'])
        ret['attachments'] = attachments
        overdue = ret.pop('overdue_status')
        dates = '<div class="task-date">Cre: ' + instance.creation_timestamp.strftime('%d-%b-%Y') + '</div>'
        if ret['due_date'] is not None:
            dates += '<div class="task-date task-'
            if overdue:
                dates += 'over'
            dates += 'due">Due: ' + instance.due_date.strftime('%d-%b-%Y') + '</div>'
        if ret['completed_date'] is not None:
            dates += '<div class="task-date task-completed">Com: ' + instance.completed_date.strftime('%d-%b-%Y') + '</div>'
        ret['dates'] = dates
        if ret['assigned_to'] is None:
            ret['assigned_to'] = instance.task_list.group.name
        else:
            ret['assigned_to'] = instance.assigned_to.profile.full_name
        return ret


class TaskListSerializer(serializers.ModelSerializer):
    task_count = serializers.IntegerField(required=False)

    class Meta:
        model = TaskList
        fields = ('id', 'name', 'group', 'task_count')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['group'] = Group.objects.get(pk=ret['group']).name
        if 'task_count' in ret:
            task_count = ret.pop('task_count')
        else:
            task_count = 0
        ret['name'] = '<div class="d-flex"><div class="align-self-start mr-auto">'+ret['name']+'</div>\
                       <div class="badge badge-primary badge-pill align-self-end">'+str(task_count)+'</div></div>'
        return ret


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ('id', 'name', 'dam_id', 'order')


class RSCollectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = rs_collection
        fields = ('ref', 'name', 'user', 'theme', 'theme2', 'theme3')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        t1 = ret.pop('theme')
        t2 = ret.pop('theme2')
        t3 = ret.pop('theme3')
        usr = ret.pop('user')
        ret['name'] = functions.get_full_collection_string(t1, t2, t3, functions.format_user(usr, 'dam'), ret['name'])
        return ret


class RSImageSerializer(serializers.ModelSerializer):
    collections = RSCollectionsSerializer(many=True, required=False)

    class Meta:
        model = rs_resource
        fields = ('ref', 'has_image', 'creation_date', 'created_by', 'field12', 'field8',
                  'field3', 'field51', 'field79', 'collections')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        try:
            ret['created_by'] = rs_user.objects.get(ref=ret['created_by']).username
        except rs_user.DoesNotExist:
            ret['created_by'] = ret['created_by']
        ret['id'] = ret['ref']
        ret['ref'] = {'ref': ret['ref'], 'url': '/images/'+str(ret['ref'])}
        return ret


class TranscriptionSerializer(serializers.ModelSerializer):
    """ Basic serializer for transcriptions """
    author = serializers.CharField(max_length=255, required=False)

    class Meta:
        model = Transcription
        fields = ('id', 'transcription', 'author', 'version')


class SimpleAttributeSerializer(serializers.ModelSerializer):
    """ Basic serializer for attribute data """
    attribute_name = serializers.StringRelatedField(source='attribute_type')
    attribute_type = serializers.PrimaryKeyRelatedField(read_only=True)
    data_type = serializers.CharField(max_length=15, source='attribute_type.data_type', read_only=True)
    options_list = serializers.CharField(max_length=15, source='attribute_type.options_list', read_only=True)

    class Meta:
        model = Attribute
        fields = ('id', 'attribute_type', 'value_STR', 'value_TXT', 'attribute_name',
                  'value_DATE_d', 'value_DATE_m', 'value_DATE_y', 'data_type', 'options_list')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.attribute_type.data_type != 'DATE':
            ret.pop('value_DATE_d')
            ret.pop('value_DATE_m')
            ret.pop('value_DATE_y')
        if instance.attribute_type.data_type != 'TXT':
            ret.pop('value_TXT')
        if instance.attribute_type.data_type != 'STR' and instance.attribute_type.data_type != 'INT':
            ret.pop('value_STR')
        return ret


class TagSerializer(serializers.ModelSerializer):
    """ Serializer for tag data """
    tag_type_name = serializers.ChoiceField(choices=Tag.TAG_TYPES, source='get_tag_type_display', required=False)

    class Meta:
        model = Tag
        fields = ('tag_type', 'tag', 'tag_group', 'tag_type_name')


class AttributeSerializer(serializers.ModelSerializer):
    """ DT serializer for attribute data """

    class Meta:
        model = Attribute
        fields = ('attribute_type', 'value_STR', 'value_TXT', 'value_INT')

    def to_representation(self, instance):
        label = instance.attribute_type.short_name
        value = str(instance)
        ret = {label: value}
        return ret


class SourceSerializer(DynamicSerializer):
    type_name = serializers.StringRelatedField(source='type', read_only=True, required=False)
    type = serializers.PrimaryKeyRelatedField(queryset=Content_type.objects.all())
    name = serializers.CharField(max_length=255)
    short_name = serializers.CharField(max_length=55, required=True)
    parent = serializers.PrimaryKeyRelatedField(queryset=Source.objects.all(), allow_null=True)
    parent_name = serializers.StringRelatedField(source='parent', read_only=True, required=False)
    attributes = AttributeSerializer(many=True, required=False)
    no_folios = serializers.IntegerField(required=False)
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Source
        fields = ('id', 'type', 'type_name', 'name', 'short_name', 'parent', 'parent_name', 'is_inventory',
                  'attributes', 'no_folios', 'tags')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        attributes = ret.pop('attributes')
        new_att = {}
        for i in attributes:
            (k, v), = i.items()
            new_att[k] = v
        ret['attributes'] = new_att
        ret['name'] = {'name': ret['name'], 'url': '/sources/'+ret['id'], 'value': ret['name']}
        parent_name = ret.pop('parent_name', None)
        if parent_name is not None:
            ret['parent'] = {'name': parent_name, 'url': '/sources/'+str(ret['parent']), 'value': ret['parent']}
        else:
            ret.pop('parent')
        type_name = ret.pop('type_name')
        ret['type'] = {'name': type_name, 'value': ret['type']}
        return ret


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
        fields = ('id', 'name')


class UserSerializer(serializers.ModelSerializer):
    """ Basic serializer for user data """
    groups = GroupSerializer(many=True, required=False)

    class Meta:
        model = User
        fields = ('id', 'last_login', 'is_superuser', 'username', 'first_name', 'last_name',
                  'email', 'is_staff', 'is_active', 'date_joined', 'groups')
        extra_kwargs = {'username': {'validators': []}}


class ProfileSerializer(serializers.ModelSerializer):
    """ Serialises user profiles and combines user data """
    user = UserSerializer(required=True)
    dam_usergroup = serializers.ChoiceField(choices=rs_user.DAM_USERGROUPS, source='get_dam_usergroup', required=False)
    wiki_groups = serializers.SerializerMethodField(required=False)
    wp_role_display = serializers.ChoiceField(choices=Profile.WP_ROLE, source='get_wp_role_display', required=False)
    dam_usergroup_display = serializers.ChoiceField(choices=rs_user.DAM_USERGROUPS, source='get_dam_usergroup_display', required=False)

    class Meta:
        model = Profile
        fields = ('id', 'full_name', 'user_id', 'dam_usergroup', 'wiki_groups', 'wp_role',
                  'user', 'wp_role_display', 'dam_usergroup_display', 'wiki_user', 'dam_user',
                  'wp_user')

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
        if self.context.get('groups') is not None:
            groups = self.context['groups']
            user.groups.clear()
            for g in groups:
                user.groups.add(g)
        return instance

    def create(self, validated_data):
        """ Create profile and user. Assumes there is a user for every profile """
        user_data = validated_data.pop('user')
        user_data.pop('groups')
        user = User.objects.create_user(**user_data)
        if self.context.get('groups') is not None:
            groups = self.context['groups']
            for g in groups:
                user.groups.add(g)
        profile = Profile.objects.create(user=user, **validated_data)
        return profile


class AttributeTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attribute_type
        fields = ('id', 'name', 'short_name', 'description', 'data_type', 'source', 'options_list', 'same_as')


class ContentXAttributeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='attribute_type.id')
    name = serializers.CharField(max_length=255, source='attribute_type.name')
    short_name = serializers.CharField(max_length=55, source='attribute_type.short_name')
    description = serializers.CharField(source='attribute_type.description')
    data_type = serializers.CharField(max_length=15, source='attribute_type.data_type')
    source = serializers.CharField(max_length=255, source='attribute_type.source')
    same_as = serializers.PrimaryKeyRelatedField(source='attribute_type.same_as', read_only=True)
    options_list = serializers.CharField(max_length=255, source='attribute_type.options_list')
    required = serializers.BooleanField()

    class Meta:
        model = Content_attributes
        fields = ('id', 'name', 'short_name', 'description', 'data_type', 'source', 'same_as', 'options_list', 'required')


class ContentTypeSerializer(serializers.ModelSerializer):
    cont_class = serializers.StringRelatedField(source='content_class', required=False)
    attribute_types = AttributeTypeSerializer(many=True, required=False)

    class Meta:
        model = Content_type
        fields = ('id', 'name', 'short_name', 'content_class', 'cont_class', 'description', 'attribute_types')
        extra_kwargs = {'name': {'validators': []}}

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if ret['content_class'] and ret['cont_class']:
            name = ret.pop('cont_class')
            ret['content_class'] = {'name': name, 'value': ret['content_class']}
        return ret


class ContentClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content_class
        fields = ('id', 'name', 'short_name', 'description')
