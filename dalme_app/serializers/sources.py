from django.contrib.auth.models import User
from dalme_app.models import Agent, Content_attributes, Set, Set_x_content, Source, Source_credit, Workflow, Work_log
from dalme_app.models._templates import get_current_user
from rest_framework import serializers
from ._common import DynamicSerializer, translate_workflow_string
from dalme_app.serializers.users import UserSerializer
from dalme_app.serializers.attributes import AttributeSerializer
from dalme_app.serializers.page import PageSerializer
from dalme_app.serializers.workflow import WorkflowSerializer
from dalme_app.serializers.sets import SetSerializer
from uuid import UUID


class SourceSetSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='set_id.id', required=True)
    name = serializers.ReadOnlyField(source='set_id.name', required=False)
    detail_string = serializers.ReadOnlyField(source='set_id.detail_string', required=False)

    class Meta:
        model = Set_x_content
        fields = ('id', 'name', 'detail_string')


class SourceCreditSerializer(DynamicSerializer):
    standard_name = serializers.ReadOnlyField(source='agent.standard_name', required=False)
    id = serializers.CharField(source='agent.id', required=True)

    class Meta:
        model = Source_credit
        fields = ('id', 'type', 'standard_name', 'note')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['type'] = {
            'id': instance.type,
            'name': instance.get_type_display()
        }
        return ret

    def to_internal_value(self, data):
        if data.get('type') is not None and type(data.get('type')) is dict:
            data['type'] = data['type']['id']
            data.pop('standard_name')
        return super().to_internal_value(data)


class SourceSerializer(DynamicSerializer):
    attributes = AttributeSerializer(many=True, required=False)
    inherited = AttributeSerializer(many=True, required=False)
    workflow = WorkflowSerializer(required=False)
    sets = SourceSetSerializer(many=True, required=False)
    pages = PageSerializer(many=True, required=False)
    owner = UserSerializer(fields=['full_name', 'username', 'id'])
    credits = SourceCreditSerializer(many=True, required=False)
    primary_dataset = SetSerializer(fields=['id', 'name', 'detail_string'], required=False)

    class Meta:
        model = Source
        fields = ('id', 'type', 'name', 'short_name', 'parent', 'has_inventory', 'primary_dataset', 'attributes', 'inherited', 'credits',
                  'no_folios', 'no_images', 'tags', 'workflow', 'owner', 'sets', 'pages', 'no_records', 'is_private')
        extra_kwargs = {
                        'parent': {'required': False},
                        'no_folios': {'required': False},
                        'no_images': {'required': False},
                        'primary_dataset': {'required': False}
                        }

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        if ret.get('attributes') is not None:
            ret['attributes'] = self.process_attributes(instance.type, ret.pop('attributes'))

        if ret.get('inherited') is not None:
            if ret['inherited'] is not None:
                ret['inherited'] = self.process_attributes(ret.pop('inherited'))

        if ret.get('parent') is not None:
            ret['parent'] = {'id': instance.parent.id, 'name': instance.parent.name}

        ret['type'] = {
            'name': instance.type.name,
            'id': instance.type.id
        }

        for k, v in dict(ret).items():
            if v is None:
                ret.pop(k)

        return ret

    def to_internal_value(self, data):
        for name in ['type', 'parent']:
            if data.get(name) is not None:
                data[name] = data[name]['id']

        if data.get('primary_dataset', {}).get('id') is not None:
            data['primary_dataset']['name'] = Set.objects.get(pk=data['primary_dataset']['id']).name

        if data.get('attributes'):
            _type = data.get('type', False) or self.instance.type
            data['attributes'] = self.process_attributes(_type, data['attributes'])

        if data.get('workflow', {}).get('status') is not None:
            if data['workflow']['status']['text'] is not None:
                for key, value in translate_workflow_string(data['workflow']['status']['text']).items():
                    data['workflow'][key] = value
            else:
                data['workflow'].pop('status')

        if data.get('credits') is not None and not data.get('credits'):
            data.pop('credits')

        for name in ['sets', 'pages']:
            if data.get(name) is not None and not data.get(name):
                data.pop(name)

        data['owner'] = {'id': data.get('owner', {}).get('id', get_current_user().id)}
        data['owner']['username'] = User.objects.get(pk=data['owner']['id']).username
        return super().to_internal_value(data)

    def run_validation(self, data):
        if data.get('type') is not None:
            required_dict = {
                12: ['name', 'short_name', 'parent', 'primary_dataset', 'attributes.authority', 'attributes.format', 'attributes.support'],
                13: ['name', 'short_name', 'parent', 'has_inventory', 'attributes.record_type', 'attributes.language'],
                19: ['name', 'short_name', 'attributes.locale']
            }
            required = required_dict.get(data['type']['id'], ['name', 'short_name'])
            missing = {}
            for field in required:
                group, field = field.split('.') if '.' in field else (None, field)
                if data.get(group, data).get(field) in [None, '', 0]:
                    missing[field] = ['This field is required.']
            if len(missing):
                raise serializers.ValidationError(missing)
            else:
                validated_data = super().run_validation(data)

                if validated_data.get('primary_dataset') is not None:
                    validated_data['primary_dataset'] = Set.objects.get(pk=validated_data['primary_dataset']['id'])

                if validated_data.get('owner') is not None:
                    validated_data['owner'] = User.objects.get(username=validated_data['owner']['username'])
        else:
            raise serializers.ValidationError({'non_field_errors': ['Type information missing.']})

        return validated_data

    def create(self, validated_data):
        attributes = validated_data.pop('attributes', None)
        workflow = validated_data.pop('workflow', None)
        pages = validated_data.pop('pages', None)
        sets = validated_data.pop('sets', None)
        credits = validated_data.pop('credits', None)

        source = Source.objects.create(**validated_data)

        self.update_or_create_attributes(source, attributes)
        self.update_or_create_workflow(source, workflow)
        self.update_or_create_pages(source, pages)
        self.update_or_create_sets(source, sets)
        self.update_or_create_credits(source, credits)

        return source

    def update(self, instance, validated_data):
        self.update_or_create_attributes(instance, validated_data.pop('attributes', None))
        self.update_or_create_workflow(instance, validated_data.pop('workflow', None))
        self.update_or_create_pages(instance, validated_data.pop('pages', None))
        self.update_or_create_sets(instance, validated_data.pop('sets', None))
        self.update_or_create_credits(instance, validated_data.pop('credits', None))

        return super().update(instance, validated_data)

    def update_or_create_attributes(self, instance, validated_data):
        if validated_data is not None:
            if instance.attributes.all().exists():
                current_attributes = instance.attributes.all()
                current_attributes_dict = dict((i.id, i) for i in current_attributes)
                active_types = list(set([i['attribute_type'] for i in validated_data]))
                new_attributes = []
                for i, attribute in enumerate(validated_data):
                    if current_attributes.filter(**attribute).count() == 1:
                        current_attributes_dict.pop(current_attributes.get(**attribute).id)
                    else:
                        new_attributes.append(attribute)

                if len(current_attributes_dict) > 0:
                    for id, attribute in current_attributes_dict.items():
                        if attribute.attribute_type in active_types:
                            attribute.delete()
            else:
                new_attributes = validated_data

            if new_attributes:
                for attribute in new_attributes:
                    instance.attributes.create(**attribute)

    def update_or_create_credits(self, instance, validated_data):
        if validated_data is not None:
            if instance.credits.all().exists():
                current_credits = instance.credits.all()
                current_credits_dict = dict((i.id, i) for i in current_credits)
                new_credits = []
                for i, credit in enumerate(validated_data):
                    if current_credits.filter(source=instance.id, agent=credit['agent']['id']).exists():
                        current_credits_dict.pop(current_credits.get(source=instance.id, agent=credit['agent']['id']).id)
                    else:
                        new_credits.append(credit)

                if len(current_credits_dict) > 0:
                    for credit in current_credits_dict.values():
                        credit.delete()
            else:
                new_credits = validated_data

            if new_credits:
                for credit in new_credits:
                    agent = Agent.objects.get(pk=credit['agent']['id'])
                    Source_credit.objects.create(
                        source=instance,
                        agent=agent,
                        note=credit.get('note'),
                        type=credit.get('type')
                    )

    def update_or_create_workflow(self, instance, validated_data):
        if validated_data is not None:
            try:
                workflow = instance.workflow
            except Workflow.DoesNotExist:
                workflow = Workflow.objects.create(source=instance, last_modified=instance.modification_timestamp)
                Work_log.objects.create(source=workflow, event='Source created', timestamp=workflow.last_modified)
            for key, value in validated_data.items():
                setattr(workflow, key, value)
            workflow.save()

    def update_or_create_pages(self, instance, validated_data):
        if validated_data is not None:
            if instance.pages.all().exists():
                new_pages = []
                current_pages = dict((i.id, i) for i in instance.pages.all())
                for page in validated_data:
                    if 'id' in page:
                        current_page = current_pages.pop(UUID(page['id']))
                        page.pop('id')
                        for key, value in page.items():
                            setattr(current_page, key, value)
                        current_page.save()
                    else:
                        new_pages.append(page)
                if len(current_pages) > 0:
                    for page in current_pages.values():
                        page.delete()
            else:
                new_pages = validated_data

            if new_pages:
                for page in new_pages:
                    instance.pages.create(**page)

    def update_or_create_sets(self, instance, validated_data):
        if validated_data is not None:
            sets = [i['set_id']['id'] for i in validated_data]
            if instance.sets.all().exists():
                current_sets = dict((i.id, i) for i in instance.sets.all())
                new_sets = []
                for set_id in sets:
                    if set_id in current_sets:
                        current_sets.pop(set_id)
                    else:
                        new_sets.append(set_id)

                if len(current_sets) > 0:
                    for set in current_sets.values():
                        set.delete()
            else:
                new_sets = sets

            if new_sets:
                for set_id in new_sets:
                    set = Set.objects.get(pk=set_id)
                    Set_x_content.objects.create(set_id=set, content_object=instance)

    def process_attributes(self, source_type, data):
        multi_attributes = [i.attribute_type.short_name for i in Content_attributes.objects.filter(content_type=source_type) if not i.unique]

        if type(data) is dict:
            attributes = []
            for key, value in data.items():
                if key in multi_attributes and value == 0:
                    continue
                value_list = value if key in multi_attributes else [value]
                for item in value_list:
                    if item is not None:
                        attributes.append({key: item})

        else:
            attributes = {}
            for attribute in data:
                if attribute is not None:
                    (key, value), = attribute.items()
                    if key in multi_attributes:
                        if attributes.get(key) is not None:
                            attributes[key].append(value)
                        else:
                            attributes[key] = [value]
                    else:
                        attributes[key] = value

        return attributes
