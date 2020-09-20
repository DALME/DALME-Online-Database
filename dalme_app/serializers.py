from django.contrib.auth.models import User, Group
from dalme_app.models import (Profile, Content_class, Content_type, Content_attributes, Set_x_content, Page, Source, TaskList, Task,
                              rs_resource, LanguageReference, rs_collection, rs_user, Transcription, Attribute, Attribute_type, GroupProperties,
                              CountryReference, LocaleReference, Tag, Attachment, Ticket, Comment, Workflow, Set, RightsPolicy)
from django_celery_results.models import TaskResult
from rest_framework import serializers
from dalme_app.utils import round_timesince
import textwrap
import datetime
import json


class DynamicSerializer(serializers.ModelSerializer):
    """ A serializer that takes an additional `fields` argument that
    indicates which fields should be included. """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)
        # Instantiate the superclass normally
        super(DynamicSerializer, self).__init__(*args, **kwargs)
        if fields is not None:
            set_fields = dict(self.fields)
            for k, v in set_fields.items():
                if k not in fields:
                    self.fields.pop(k)


class GroupPropertiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupProperties
        fields = ('type', 'description')


class GroupSerializer(serializers.ModelSerializer):
    """ Basic serializer for user group data """
    properties = GroupPropertiesSerializer()

    class Meta:
        model = Group
        fields = ('id', 'name', 'properties')


class ProfileSerializer(DynamicSerializer):
    """ Serialises user profiles """
    class Meta:
        model = Profile
        fields = ('full_name',)


class UserSerializer(DynamicSerializer):
    """ Serializes user and profile data """
    groups = GroupSerializer(many=True, required=False)
    last_login = serializers.DateTimeField(format='%d-%b-%Y@%H:%M', required=False)
    date_joined = serializers.DateTimeField(format='%d-%b-%Y@%H:%M', required=False)
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'last_login', 'is_superuser', 'username', 'first_name', 'last_name',
                  'email', 'is_staff', 'is_active', 'date_joined', 'groups', 'profile')
        extra_kwargs = {'username': {'validators': []}}

    def update(self, instance, validated_data):
        if validated_data.get('profile') is not None:
            profile_data = validated_data.pop('profile')
            profile = instance.profile
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()
        return super().update(instance, validated_data)

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create_user(**validated_data)
        Profile.objects.create(user=user, **profile_data)
        return user


class AgentSerializer(DynamicSerializer):
    user = UserSerializer(fields=['full_name', 'username', 'id'])

    class Meta:
        model = Agent
        fields = ('id', 'type', 'standard_name', 'notes', 'user')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['type'] = {
            'id': instance.type,
            'name': instance.get_type_display()
        }
        return ret


class AsyncTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskResult
        fields = '__all__'


class AttachmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Attachment
        fields = '__all__'


class AttributeSerializer(serializers.ModelSerializer):
    """ DT serializer for attribute data """

    class Meta:
        model = Attribute
        fields = ('attribute_type', 'value_STR', 'value_TXT', 'value_INT', 'value_DATE_d', 'value_DATE_m', 'value_DATE_y')

    def to_representation(self, instance):
        label = instance.attribute_type.short_name
        if instance.attribute_type.data_type == 'UUID':
            data = json.loads(instance.value_STR)
            object = eval('{}.objects.get(pk="{}")'.format(data['class'], data['id']))
            ret = {label: {
                'name': object.name,
                'url': object.get_url(),
                'value': instance.value_STR
            }}
        elif instance.attribute_type.data_type == 'DATE':
            ret = {label: {
                'name': str(instance),
                'value': {
                    'd': instance.value_DATE_d,
                    'm': instance.value_DATE_m,
                    'y': instance.value_DATE_y
                }}}
        else:
            ret = {label: str(instance)}
        return ret


class AttributeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute_type
        fields = ('id', 'name', 'short_name', 'description', 'data_type', 'source', 'options_list', 'same_as')


class CommentSerializer(serializers.ModelSerializer):
    creation_timestamp = serializers.DateTimeField(format='%-d-%b-%Y@%H:%M')

    class Meta:
        model = Comment
        fields = ('body', 'creation_timestamp')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['user'] = '<a href="/users/{}">{}</a>'.format(instance.creation_user.username, instance.creation_user.profile.full_name)
        if instance.creation_user.profile.profile_image is not None:
            ret['avatar'] = '<img src="{}" class="img_avatar" alt="avatar">'.format(instance.creation_user.profile.profile_image)
        else:
            ret['avatar'] = '<i class="fa fa-user-alt-slash img_avatar mt-1 fa-2x"></i>'
        return ret


class ContentClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content_class
        fields = ('id', 'name', 'short_name', 'description')


class ContentTypeSerializer(DynamicSerializer):
    cont_class = serializers.StringRelatedField(source='content_class', required=False)
    attribute_types = AttributeTypeSerializer(many=True, required=False)

    class Meta:
        model = Content_type
        fields = ('id', 'name', 'short_name', 'content_class', 'cont_class', 'description', 'attribute_types', 'has_pages', 'parents', 'has_inventory', 'r1_inheritance', 'r2_inheritance')
        extra_kwargs = {'name': {'validators': []}}

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if ret.get('content_class') is not None and ret.get('cont_class') is not None:
            name = ret.pop('cont_class')
            ret['content_class'] = {'name': name, 'value': ret['content_class']}
        if ret.get('parents') is not None:
            ctype_dict = {i.id: i.name for i in Content_type.objects.all()}
            list_ids = ret['parents'].split(',') if ',' in ret['parents'] else [ret['parents']]
            ret['parents'] = [{'id': int(i), 'name': ctype_dict[int(i)]} for i in list_ids]
        return ret


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


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryReference
        fields = ('id', 'name', 'alpha_2_code', 'alpha_3_code', 'num_code')


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = LanguageReference
        fields = ('id', 'glottocode', 'iso6393', 'name', 'type', 'parent')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if ret.get('parent') is not None:
            ret['parent'] = {
                'name': instance.parent.name,
                'id': instance.parent.id
                }
        return ret


class LocaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocaleReference
        fields = ('id', 'name', 'administrative_region', 'country')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if ret.get('country') is not None:
            ret['country'] = {
                'name': instance.country.name,
                'id': instance.country.id
                }
        return ret


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ('id', 'name', 'dam_id', 'order')


class RightsSerializer(serializers.ModelSerializer):
    rights_status_name = serializers.ChoiceField(choices=RightsPolicy.RIGHTS_STATUS, source='get_rights_status_display', required=False)
    url = serializers.ReadOnlyField(source='get_url', read_only=True, required=False)

    class Meta:
        model = RightsPolicy
        fields = ('id', 'name', 'url', 'rights_holder', 'rights_status', 'rights_status_name', 'rights', 'notice_display', 'rights_notice', 'licence', 'attachments')
        extra_kwargs = {
                        'rights_notice': {'required': False},
                        'licence': {'required': False},
                        'attachments': {'required': False}
                        }

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if ret['attachments'] is not None:
            a_pill = '<a href="/download/{}" class="task-attachment">File</a>'.format(instance.attachments.file)
            ret['attachments'] = {
                'pill': a_pill,
                'file': {
                    'file_id': ret.pop('attachments'),
                    'filename': instance.attachments.filename
                }
            }
        ret['name'] = {
            'name': ret.pop('name'),
            'url': ret.pop('url')
        }
        ret['rights_status'] = {
            'name': ret.pop('rights_status_name'),
            'value': ret.pop('rights_status')
        }
        return ret


class RSCollectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = rs_collection
        fields = ('ref', 'name', 'user', 'theme', 'theme2', 'theme3')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        t_fields = [ret.pop(i) for i in ['theme', 'theme2', 'theme3']]
        ret['name'] = '≫'.join(t_fields)
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


class SetSerializer(DynamicSerializer):
    owner = UserSerializer(fields=['id', 'full_name', 'username'])
    set_type_name = serializers.CharField(source='get_set_type_display', required=False)
    permissions_name = serializers.CharField(source='get_permissions_display', required=False)
    dataset_usergroup = GroupSerializer()

    class Meta:
        model = Set
        fields = ('id', 'name', 'set_type', 'set_type_name', 'description', 'owner', 'permissions', 'permissions_name', 'workset_progress', 'member_count', 'endpoint', 'creation_timestamp', 'is_public',
                  'has_landing', 'stat_title', 'stat_text', 'dataset_usergroup', 'detail_string')
        # extra_kwargs = {'set_type_label': {'required': False}, 'permissions_label': {'required': False}}

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if ret.get('workset_progress') is not None and ret['set_type'] == 4:
            ret['workset'] = '<a class="workset-title" href="/sets/go/{}">{}</a><div class="workset-description">{}</div><div class="workset-endpoint">Endpoint: {}</div>'.format(ret['id'], ret['name'], ret['description'], ret['endpoint'])
            progress = ret['workset_progress']
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
        ret['set_type'] = {
            'name': ret.pop('set_type_name'),
            'value': ret.pop('set_type')
        }
        ret['permissions'] = {
            'name': ret.pop('permissions_name'),
            'value': ret.pop('permissions')
        }
        return ret


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
        if instance.attribute_type.data_type != 'STR' and instance.attribute_type.data_type != 'INT' and instance.attribute_type.data_type != 'UUID':
            ret.pop('value_STR')
        return ret


class TagSerializer(serializers.ModelSerializer):
    """ Serializer for tag data """
    tag_type_name = serializers.ChoiceField(choices=Tag.TAG_TYPES, source='get_tag_type_display', required=False)

    class Meta:
        model = Tag
        fields = ('tag_type', 'tag', 'tag_group', 'tag_type_name')
        extra_kwargs = {'tag_type': {'required': False}}


class TaskSerializer(serializers.ModelSerializer):
    creation_timestamp = serializers.DateTimeField(format='%d-%b-%Y', required=False)
    completed_date = serializers.DateField(format='%d-%b-%Y', required=False, allow_null=True)
    due_date = serializers.DateField(format='%d-%b-%Y', required=False, allow_null=True)

    class Meta:
        model = Task
        fields = ('id', 'title', 'task_list', 'due_date', 'completed', 'completed_date', 'created_by', 'assigned_to', 'description',
                  'workset', 'url', 'creation_timestamp', 'overdue_status', 'file')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['comment_count'] = instance.comments.count()
        task = '<div class="d-flex align-items-center mb-1"><a href="/tasks/{}" class="task-title">{}</a>'.format(ret['id'], ret['title'])
        if ret['comment_count'] > 0:
            task += '<div class="align-self-end ml-auto d-flex mr-2 align-items-center"><i class="fas fa-comment fa-lg icon-badge">\
            </i><span class="icon-badge-count">{}</span></div>'.format(ret['comment_count'])
        task += '</div><div class="task-description">{}</div>'.format(ret['description'])
        ret['task'] = task
        attachments = ''
        attachments_detail = ''
        if ret['workset'] is not None:
            attachments += '<a href="/sets/{}" class="task-attachment">Workset</a>'.format(ret['workset'])
            attachments_detail += '<a href="/sets/{}" class="task-attachment">Workset: {}</a>'.format(ret['workset'], instance.workset.name)
        if ret['url'] is not None:
            attachments += '<a href="{}" class="task-attachment">URL</a>'.format(ret['url'])
            attachments_detail += '<a href="{}" class="task-attachment">URL: {}</a>'.format(ret['url'], textwrap.shorten(instance.url, width=35, placeholder="..."))
        if ret['file'] is not None:
            attachments += '<a href="/download/{}" class="task-attachment">File</a>'.format(instance.file.file)
            attachments_detail += '<a href="/download/{}" class="task-attachment">File: {}</a>'.format(instance.file.file, instance.file.filename)
        ret['attachments'] = attachments
        ret['attachments_detail'] = attachments_detail
        overdue = ret.pop('overdue_status')
        dates = '<div class="task-date">Cre: ' + ret['creation_timestamp'] + '</div>'
        dates_detail = '<span class="task-date">Created: ' + ret['creation_timestamp'] + ' by '+instance.creation_user.username+'</span>'
        if ret['due_date'] is not None:
            dates += '<div class="task-date task-'
            dates_detail += '<span class="task-date task-'
            if overdue:
                dates += 'over'
                dates_detail += 'over'
            dates += 'due">Due: ' + ret['due_date'] + '</div>'
            dates_detail += 'due">Due: ' + ret['due_date'] + '</span>'
        if ret['completed_date'] is not None:
            dates += '<div class="task-date task-completed">Com: ' + ret['completed_date'] + '</div>'
            dates_detail += '<span class="task-date task-completed">Completed: ' + ret['completed_date'] + '</span>'
        ret['dates'] = dates
        ret['dates_detail'] = dates_detail
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


class TicketSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)
    creation_timestamp = serializers.DateTimeField(format='%d-%b-%Y@%H:%M', required=False)

    class Meta:
        model = Ticket
        fields = ('id', 'subject', 'description', 'status', 'tags', 'url', 'file',
                  'creation_user', 'creation_timestamp')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['comment_count'] = instance.comments.count()
        ticket = '<div class="d-flex align-items-center"><i class="fa fa-exclamation-circle ticket-status-{} fa-fw"></i>'.format(ret['status'])
        ticket += '<a href="/tickets/'+str(ret['id'])+'" class="ticket_subject">'+ret['subject']+'</a>'
        if ret['comment_count'] > 0:
            ticket += '<i class="fas fa-comment fa-lg icon-badge ml-2"></i><span class="icon-badge-count">{}</span></div>'.format(ret['comment_count'])
        ret['ticket'] = ticket
        attachments = ''
        if ret['url'] is not None:
            attachments += '<a href="{}" class="task-attachment">URL</a>'.format(ret['url'])
        if ret['file'] is not None:
            attachments += '<a href="/download/{}" class="task-attachment">File</a>'.format(instance.file.file)
        ret['attachments'] = attachments
        tags = ret.pop('tags', None)
        tag_string = ''
        for tag in tags:
            if tag['tag'] != '0' and tag['tag'] != '':
                tag_string += '<div class="ticket-tag ticket-{}">{}</div>'.format(tag['tag'], tag['tag'])
        ret['tags'] = tag_string
        return ret


class TranscriptionSerializer(serializers.ModelSerializer):
    """ Basic serializer for transcriptions """
    author = serializers.CharField(max_length=255, required=False)

    class Meta:
        model = Transcription
        fields = ('id', 'transcription', 'author', 'version')


class WorkflowSerializer(serializers.ModelSerializer):
    """Basic serializer for workflow control"""
    last_user = UserSerializer(fields=['username', 'profile'])

    class Meta:
        model = Workflow
        fields = ('help_flag', 'is_public', 'last_modified', 'last_user', 'wf_status', 'stage', 'status')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        tstamp = ret.pop('last_modified')
        last_user = ret.pop('last_user')
        ret['activity'] = {
            # version of code that needs Python 3.7 to work
            # 'timestamp': round_timesince(datetime.datetime.fromisoformat(ret.pop('last_modified'))),
            # version for Python 3.6 (has to remove : from utcoffset because ISO standard is not properly implemented)
            'timestamp': round_timesince(datetime.datetime.strptime(tstamp[0:-3:]+tstamp[-2::], '%Y-%m-%dT%H:%M:%S.%f%z')),
            'user': last_user['profile']['full_name'],
            'username': last_user['username']
        }
        return ret


def translate_workflow_status(data):
    stage_by_no = dict(Workflow.PROCESSING_STAGES)
    stage_by_name = {label: number for number, label in stage_by_no.items()}
    if type(data) is str:
        str_elements = data.split(' ')
        if len(str_elements) == 1:
            return {'wf_status': 1}
        elif len(str_elements) == 2:
            return {'wf_status': 3, 'stage': stage_by_name[str_elements[1]] + 1}
        elif len(str_elements) == 3:
            return {'wf_status': 2, 'stage': stage_by_name[str_elements[0]]}
        else:
            raise ValueError('Incorrect data supplied: invalid text string.')
    elif type(data) is dict:
        if data.get('wf_status') is not None and data.get('stage') is not None:
            if data['wf_status'] == 1:
                return 'assessing'
            elif data['wf_status'] == 2:
                return '{} in progress'.format(stage_by_no[data['stage']])
            elif data['wf_status'] == 3:
                return 'awaiting {}'.format(stage_by_no[data['stage'] + 1])
            else:
                raise ValueError('Incorrect data supplied: invalid wf_status value.')
        else:
            raise ValueError('Incorrect data supplied: dict must contain keys wf_status and stage.')
    else:
        raise ValueError('Incorrect data supplied: must be string or dict.')


class SourceSetSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='set_id.name', read_only=True, required=False)
    detail_string = serializers.ReadOnlyField(source='set_id.detail_string', read_only=True, required=False)

    class Meta:
        model = Set_x_content
        fields = ('set_id', 'name', 'detail_string')
class SourceCreditSerializer(DynamicSerializer):
    agent = serializers.ReadOnlyField(source='agent.standard_name', read_only=True, required=False)
    agent_id = serializers.ReadOnlyField(source='agent.id', read_only=True, required=False)
    notes = serializers.ReadOnlyField(source='agent.notes', read_only=True, required=False)

    class Meta:
        model = Source_credit
        fields = ('id', 'type', 'agent', 'agent_id', 'notes')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['type'] = {
            'id': instance.type,
            'name': instance.get_type_display()
        }
        ret['agent'] = {
            'id': ret.pop('agent_id'),
            'standard_name': ret['agent']
        }
        return ret


class SourceSerializer(DynamicSerializer):
    attributes = AttributeSerializer(many=True, required=False)
    inherited = AttributeSerializer(many=True, required=False)
    tags = TagSerializer(many=True, required=False)
    workflow = WorkflowSerializer(required=False)
    sets = SourceSetSerializer(many=True, required=False)
    type = ContentTypeSerializer(fields=['id', 'name'])
    pages = PageSerializer(many=True, required=False)
    credits = SourceCreditSerializer(many=True, required=False)

    class Meta:
        model = Source
        fields = ('id', 'type', 'name', 'short_name', 'parent', 'has_inventory', 'primary_dataset', 'attributes', 'inherited', 'credits',
                  'no_folios', 'no_images', 'tags', 'workflow', 'owner', 'primary_dataset', 'sets', 'pages', 'no_records', 'is_private')
        extra_kwargs = {
                        'parent': {'required': False},
                        'no_folios': {'required': False},
                        'no_images': {'required': False},
                        'primary_dataset': {'required': False}
                        }

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if ret.get('attributes') is not None:
            ret['attributes'] = self.process_attributes(ret.pop('attributes'), instance)
        if ret.get('inherited') is not None:
            if ret['inherited'] is not None:
                ret['inherited'] = self.process_attributes(ret.pop('inherited'))
        if ret.get('parent') is not None:
            if ret['parent']:
                ret['parent'] = {'id': ret['parent'], 'name': instance.parent.name}
        if ret.get('owner') is not None:
            ret['owner'] = {
                'id': instance.owner.id,
                'username': instance.owner.username,
                'full_name': instance.owner.profile.full_name
            }
        for k, v in dict(ret).items():
            if v is None:
                ret.pop(k)
        return ret

    def to_internal_value(self, data):
        if 'attributes' in data:
            multi_attributes = [i.attribute_type.short_name for i in Content_attributes.objects.filter(content_type=self.instance.type) if not i.unique]
            deserialised = []
            for key, value in data['attributes'].items():
                att_type = Attribute_type.objects.get(short_name=key)
                if key in multi_attributes and value == 0:
                    continue
                value_list = value if key in multi_attributes else [value]
                for v in value_list:
                    att = {'attribute_type': att_type.id}
                    if att_type.data_type == 'INT':
                        att['value_INT'] = int(v)
                    elif att_type.data_type == 'TXT':
                        att['value_TXT'] = v
                    elif att_type.data_type == 'DATE':
                        att['value_DATE_d'] = v['d']
                        att['value_DATE_m'] = v['m']
                        att['value_DATE_y'] = v['y']
                    else:
                        att['value_STR'] = v
                    deserialised.append(att)
            data['attributes'] = deserialised
        if 'pages' in data:
            if data['pages'].get('0') is not None:
                data['pages'] = self.deserialise_numbered_dict(data['pages'])
            else:
                data['pages'] = [data['pages']]
        if 'sets' in data:
            if data['sets'].get('0') is not None:
                data['sets'] = self.deserialise_numbered_dict(data['sets'])
            else:
                data['sets'] = [data['sets']]
        if 'parent' in data:
            data['parent'] = data['parent']['id']
        if 'workflow' in data:
            if data['workflow'].get('status') is not None:
                text = data['workflow']['status']['text']
                values = translate_workflow_status(text)
                data['workflow']['wf_status'] = values['wf_status']
                data['workflow']['stage'] = values['stage']
        if 'owner' in data:
            data['owner'] = data['owner']['id']
        return super().to_internal_value(data)

    def create(self, validated_data):
        if validated_data.get('attributes') is not None:
            attributes_data = validated_data.pop('attributes')
        if validated_data.get('workflow') is not None:
            workflow_data = validated_data.pop('workflow')
        if validated_data.get('pages') is not None:
            pages_data = validated_data.pop('pages')
        if validated_data.get('sets') is not None:
            sets_list = [i['set_id'] for i in validated_data.pop('sets')]

        source = Source.objects.create(**validated_data)

        if attributes_data:
            for attribute in attributes_data:
                source.attributes.create(**attribute)

        if workflow_data:
            workflow = source.workflow
            if workflow_data.get('status') is not None:
                status_data = translate_workflow_status(workflow_data['status'])
                workflow.wf_status = status_data.get('wf_status', workflow.wf_status)
                workflow.stage = status_data.get('stage', workflow.stage)
            workflow.help_flag = workflow_data.get('help_flag', workflow.help_flag)
            workflow.is_public = workflow_data.get('is_public', workflow.is_public)
            workflow.save()

        if pages_data:
            for page in pages_data:
                source.pages.create(**page)

        if sets_list:
            for _set in sets_list:
                Set_x_content.objects.create(set_id=_set, content_object=source)

        return source

    def update(self, instance, validated_data):
        if validated_data.get('attributes') is not None:
            attributes_data = validated_data.pop('attributes')
            multi_attributes = [i.attribute_type for i in Content_attributes.objects.filter(content_type=instance.type) if not i.unique]
            attributes = {}
            for attribute in attributes_data:
                if attribute['attribute_type'] in multi_attributes:
                    if attributes.get(attribute['attribute_type']) is not None:
                        attributes[attribute['attribute_type']].append(attribute)
                    else:
                        attributes[attribute['attribute_type']] = [attribute]
                else:
                    attributes[attribute['attribute_type']] = attribute

            current_attributes = instance.attributes.all()
            control = []

            for att_type, attribute_dict in attributes.items():
                if type(attribute_dict) is list:
                    current_attributes.filter(attribute_type=att_type).delete()
                    for att in attribute_dict:
                        na = instance.attributes.create(**att)
                        control.append(na.id)
                else:
                    if current_attributes.filter(**attribute_dict).exists():
                        control.append(current_attributes.get(**attribute_dict).id)
                    elif current_attributes.filter(attribute_type=att_type).count() > 0:
                        attribute = current_attributes.get(attribute_type=att_type)
                        attribute_dict.pop('attribute_type')
                        for attr, value in attribute_dict.items():
                            setattr(attribute, attr, value)
                        attribute.save()
                        control.append(attribute.id)
                    else:
                        na = instance.attributes.create(**attribute_dict)
                        control.append(na.id)

            for attribute in current_attributes:
                if attribute.id not in control:
                    attribute.delete()

        if validated_data.get('workflow') is not None:
            workflow_data = validated_data.pop('workflow')
            workflow = instance.workflow
            if workflow_data.get('status') is not None:
                status_data = translate_workflow_status(workflow_data['status'])
                workflow.wf_status = status_data.get('wf_status', workflow.wf_status)
                workflow.stage = status_data.get('stage', workflow.stage)
            workflow.help_flag = workflow_data.get('help_flag', workflow.help_flag)
            workflow.is_public = workflow_data.get('is_public', workflow.is_public)
            workflow.save()

        if validated_data.get('pages') is not None:
            pages_data = validated_data.pop('pages')
            current_pages = instance.pages.all()
            control = []
            for page_dict in pages_data:
                if current_pages.filter(**page_dict).exists():
                    control.append(current_pages.get(**page_dict).id)
                else:
                    if page_dict.get('id') is not None:
                        page = current_pages.get(pk=page_dict['id'])
                        for attr, value in page_dict.items():
                            setattr(page, attr, value)
                        page.save()
                        control.append(page.id)
                    else:
                        np = instance.pages.create(**page_dict)
                        control.append(np.id)
            for page in current_pages:
                if page.id not in control:
                    page.delete()

        if validated_data.get('sets') is not None:
            sets_list = [i['set_id'] for i in validated_data.pop('sets')]
            current_sets_list = [i.set_id for i in instance.sets.all()]
            for _set in sets_list:
                if _set not in current_sets_list:
                    Set_x_content.objects.create(set_id=_set, content_object=instance)
            for _set in current_sets_list:
                if _set not in sets_list:
                    instance.sets.get(set_id=_set.id).delete()

        return super().update(instance, validated_data)

    def deserialise_numbered_dict(self, data):
        deserialised = []
        for key, value in data.items():
            deserialised.append(value)
        return deserialised

    def process_attributes(self, qset, instance):
        result = {}
        multi_attributes = [i.attribute_type.short_name for i in Content_attributes.objects.filter(content_type=instance.type) if not i.unique]
        for i in qset:
            (k, v), = i.items()
            if k in multi_attributes:
                if result.get(k) is not None:
                    result[k].append(v)
                else:
                    result[k] = [v]
            else:
                result[k] = v
        return result
