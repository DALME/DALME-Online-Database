"""Serializers for record data."""

from rest_framework import serializers

from domain.api.resources.agents import AgentSerializer
from domain.api.resources.attributes import AttributeSerializer
from domain.api.resources.languages import LanguageReferenceSerializer
from domain.api.resources.locales import LocaleReferenceSerializer
from domain.api.resources.pages import PageSerializer
from domain.api.resources.users import UserSerializer
from domain.api.resources.workflows import WorkflowSerializer
from domain.api.serializers import DynamicSerializer
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

    attributes = AttributeSerializer(many=True, required=False)
    workflow = WorkflowSerializer(required=False)
    pages = PageSerializer(many=True, required=False)
    page_info = PageSerializer(field_set='info', many=True, required=False)
    owner = UserSerializer(field_set='attribute', required=False)
    creation_user = UserSerializer(field_set='attribute', required=False)
    modification_user = UserSerializer(field_set='attribute', required=False)
    image_urls = serializers.SerializerMethodField(required=False)
    collections = RecordAttributeCollectionSerializer(many=True, required=False)
    parent = RecordParentSerializer(required=False)
    # annotated fields
    description = serializers.ReadOnlyField(required=False)
    record_type = RecordTypeSerializer(field_set='attribute')
    locale = LocaleReferenceSerializer(many=True, required=False)
    language = LanguageReferenceSerializer(many=True, required=False)
    # method fields
    agents = AgentSerializer(many=True, required=False)
    credit_line = serializers.SerializerMethodField(required=False)
    credits = serializers.SerializerMethodField(required=False)
    source = serializers.SerializerMethodField(required=False)
    date = serializers.SerializerMethodField(required=False)

    class Meta:
        model = Record
        fields = [
            'id',
            'name',
            'short_name',
            'owner',
            'attributes',
            'no_folios',
            'has_images',
            'no_images',
            'workflow',
            'pages',
            'page_info',
            'is_private',
            'comment_count',
            'creation_timestamp',
            'creation_user',
            'modification_timestamp',
            'modification_user',
            'has_transcriptions',
            'no_transcriptions',
            'image_urls',
            'description',
            'record_type',
            'date',
            'collections',
            'locale',
            'language',
            'credit_line',
            'credits',
            'source',
            'agents',
            'parent',
        ]
        default_exclude = [
            'has_images',
            'has_transcriptions',
            'no_transcriptions',
            'image_urls',
            'description',
            'record_type',
            'date',
            'collections',
            'locale',
            'language',
            'credit_line',
            'credits',
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
                'id',
                'name',
                'short_name',
                'owner',
                'attributes',
                'no_folios',
                'is_private',
                'comment_count',
                'creation_timestamp',
                'creation_user',
                'modification_timestamp',
                'modification_user',
                'date',
                'collections',
                'locale',
                'language',
                'source',
                'workflow',
            ],
            'retrieve': [
                'id',
                'name',
                'short_name',
                'owner',
                'attributes',
                'no_folios',
                'workflow',
                'pages',
                'is_private',
                'comment_count',
                'creation_timestamp',
                'creation_user',
                'modification_timestamp',
                'modification_user',
                'no_transcriptions',
                'collections',
                'credit_line',
                'parent',
                'agents',
            ],
            'web': [
                'id',
                'name',
                'short_name',
                #'parent',
                #'parent_name',
                'no_folios',
                'no_images',
                'no_transcriptions',
                'collections',
                'has_images',
                'has_transcriptions',
                'description',
                'record_type',
                'date',
            ],
            'web_detail': [
                'locale',
                'language',
                'credit_line',
                'credits',
                'source',
                'agents',
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
