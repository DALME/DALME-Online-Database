"""Serializers for record data."""

from rest_framework import serializers

from domain.api.resources.agents import AgentSerializer
from domain.api.resources.attributes import AttributeSerializer
from domain.api.resources.languages import LanguageReferenceSerializer
from domain.api.resources.locales import LocaleReferenceSerializer
from domain.api.resources.pages import PageSerializer
from domain.api.resources.users import UserSerializer
from domain.api.resources.workflows import WorkflowSerializer
from domain.api.serializers import DynamicSerializer, PermissionsSerializer
from domain.models import Collection, Record, RecordType, Workflow
from domain.models.resourcespace import rs_resource


def translate_workflow_string(data):
    """Return a normalized version of the workflow status string."""
    stage_by_no = dict(Workflow.PROCESSING_STAGES)
    status_by_no = dict(Workflow.WORKFLOW_STATUS)
    stage_by_name = {label: number for number, label in stage_by_no.items()}
    status_by_name = {label: number for number, label in status_by_no.items()}

    if isinstance(data, str):
        str_elements = data.strip().split(' ')
        if len(str_elements) == 1:
            status = status_by_name[str_elements[0].strip().lower()]

            if status == 1:
                return {'wf_status': status}

            if status == 3:  # noqa: PLR2004
                return {
                    'wf_status': status,
                    'stage': 5,
                    'ingestion_done': True,
                    'transcription_done': True,
                    'markup_done': True,
                    'review_done': True,
                    'parsing_done': True,
                }

        elif len(str_elements) == 2:  # noqa: PLR2004
            stage_name = str_elements[1].strip().lower()
            stage = stage_by_name[stage_name] - 1
            value = {'wf_status': 2, 'stage': stage}

            for i in range(1, 6):
                value[stage_by_no[i] + '_done'] = i <= stage

            return value

        elif len(str_elements) == 3:  # noqa: PLR2004
            stage_name = str_elements[0].strip().lower()
            stage = stage_by_name[stage_name]
            value = {'wf_status': 2, 'stage': stage}

            for i in range(1, 6):
                value[stage_by_no[i] + '_done'] = i < stage

            return value

    return None


class RecordTypeSerializer(DynamicSerializer):
    """Serializer for record types."""

    class Meta:
        model = RecordType
        fields = ['id', 'label']
        field_sets = {
            'attribute': [
                'id',
                'label',
            ],
        }


class RecordAttributeCollectionSerializer(serializers.ModelSerializer):
    """Serializes collections as attributes of records."""

    id = serializers.ReadOnlyField(source='col_id')
    name = serializers.ReadOnlyField(source='col_name')

    class Meta:
        model = Collection
        fields = ['id', 'name']


class RecordParentSerializer(serializers.BaseSerializer):
    """Serializer for record parent instances (either RecordGroup or Publication)."""

    def to_representation(self, data):
        """Override method to use serializer class instead of instance."""
        model_name = data._meta.model.__name__  # noqa: SLF001
        serializer_class_name = f'{model_name}Serializer'
        srs = __import__('domain.api.resources', fromlist=[serializer_class_name])  # noqa: F841
        self.serializer_class = eval(f'srs.{serializer_class_name}')
        ret = self.serializer_class(data, field_set='parent').data
        ret['type'] = model_name
        return ret


class RecordSerializer(DynamicSerializer):
    """Serializer for records."""

    agents = AgentSerializer(many=True, required=False)
    agent_ids = serializers.PrimaryKeyRelatedField(source='agents', required=False, read_only=True, many=True)
    attributes = AttributeSerializer(many=True, required=False)
    attribute_ids = serializers.PrimaryKeyRelatedField(source='attributes', required=False, read_only=True, many=True)
    collections = RecordAttributeCollectionSerializer(many=True, required=False)
    creation_user = UserSerializer(field_set='attribute', required=False)
    creation_user_id = serializers.PrimaryKeyRelatedField(source='creation_user', required=False, read_only=True)
    image_urls = serializers.SerializerMethodField(required=False)
    modification_user = UserSerializer(field_set='attribute', required=False)
    modification_user_id = serializers.PrimaryKeyRelatedField(
        source='modification_user', required=False, read_only=True
    )
    owner = UserSerializer(field_set='attribute', required=False)
    owner_id = serializers.PrimaryKeyRelatedField(source='owner', required=False, read_only=True)
    page_info = PageSerializer(field_set='info', many=True, required=False)
    pages = PageSerializer(many=True, required=False)
    parent = RecordParentSerializer(required=False)
    # places = PlaceSerializer(many=True, required=False)
    place_ids = serializers.PrimaryKeyRelatedField(source='places', required=False, read_only=True, many=True)
    workflow = WorkflowSerializer(required=False)
    # annotated fields
    description = serializers.ReadOnlyField(required=False)
    language = LanguageReferenceSerializer(many=True, required=False)
    locale = LocaleReferenceSerializer(many=True, required=False)
    record_type = RecordTypeSerializer(field_set='attribute')
    # method fields
    credit_line = serializers.SerializerMethodField(required=False)
    credits = serializers.SerializerMethodField(required=False)
    date = serializers.SerializerMethodField(required=False)
    permissions = serializers.SerializerMethodField(required=False)
    source = serializers.SerializerMethodField(required=False)
    collection_ids = serializers.SerializerMethodField(required=False)

    class Meta:
        model = Record
        fields = [
            'agents',
            'agent_ids',
            'attributes',
            'attribute_ids',
            'collections',
            'collection_ids',
            'comment_count',
            'creation_timestamp',
            'creation_user',
            'creation_user_id',
            'credit_line',
            'credits',
            'date',
            'description',
            'has_images',
            'has_transcriptions',
            'id',
            'image_urls',
            'is_private',
            'language',
            'locale',
            'modification_timestamp',
            'modification_user',
            'modification_user_id',
            'name',
            'no_folios',
            'no_images',
            'no_transcriptions',
            'owner',
            'owner_id',
            'page_info',
            'pages',
            'parent',
            'permissions',
            'places',
            'place_ids',
            'record_type',
            'short_name',
            'source',
            'workflow',
        ]
        default_exclude = [
            'collections',
            'credit_line',
            'credits',
            'date',
            'description',
            'has_images',
            'has_transcriptions',
            'image_urls',
            'language',
            'locale',
            'no_transcriptions',
            'record_type',
            'source',
        ]
        field_sets = {
            'attribute': [
                'id',
                'name',
                'short_name',
            ],
            'collection_member': [
                'id',
                'name',
            ],
            'option': [
                'id',
                'name',
            ],
            'list': [
                'attributes',
                'collections',
                'comment_count',
                'creation_timestamp',
                'creation_user',
                'date',
                'id',
                'is_private',
                'language',
                'locale',
                'modification_timestamp',
                'modification_user',
                'name',
                'no_folios',
                'owner',
                'short_name',
                'source',
                'workflow',
            ],
            'retrieve': [
                # 'agents',
                'agent_ids',
                'attribute_ids',
                'collection_ids',
                'comment_count',
                'creation_timestamp',
                'creation_user_id',
                'credit_line',
                'id',
                'is_private',
                'modification_timestamp',
                'modification_user_id',
                'name',
                'no_folios',
                'no_transcriptions',
                # 'owner',
                'owner_id',
                'pages',
                'parent',
                'permissions',
                'place_ids',
                'short_name',
                'workflow',
            ],
            'web': [
                'collections',
                'date',
                'description',
                'has_images',
                'has_transcriptions',
                'id',
                'name',
                'no_folios',
                'no_images',
                'no_transcriptions',
                'record_type',
                'short_name',
                #'parent_name',
                #'parent',
            ],
            'web_detail': [
                'agents',
                'credit_line',
                'credits',
                'language',
                'locale',
                'source',
            ],
            'images': ['image_urls'],
        }

    def get_image_urls(self, obj):
        try:
            img_id = obj.pages.exclude(dam_id__isnull=True).first().dam_id
            return rs_resource.objects.get(ref=img_id).get_image_url('scr,thm')
        except (KeyError, ValueError, AttributeError):
            return None

    def get_credit_line(self, obj):
        return obj.get_credit_line()

    def get_credits(self, obj):
        return obj.get_credits()

    def get_source(self, obj):
        return obj.get_source()

    def get_date(self, obj):
        return obj.get_date()

    def get_permissions(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            perms = obj.get_user_permissions(request.user)
            serializer = PermissionsSerializer(perms)
            return serializer.data
        return None

    def get_collection_ids(self, obj):
        return [x.collection_id for x in obj.collections.all()]
