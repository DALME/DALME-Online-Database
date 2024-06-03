"""Serializers for record data."""

from rest_framework import serializers

from api.dynamic_serializer import DynamicSerializer
from api.resources.attributes import AttributeSerializer
from api.resources.pages import PageSerializer
from api.resources.users import UserSerializer
from api.resources.workflows import WorkflowSerializer
from ida.models import Collection, Record, RecordType, Workflow
from ida.models.resourcespace import rs_resource


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
    """Serializer collections as attributes of records."""

    id = serializers.ReadOnlyField(source='col_id')
    name = serializers.ReadOnlyField(source='col_name')

    class Meta:
        model = Collection
        fields = ['id', 'name']


class RecordSerializer(DynamicSerializer):
    """Serializer for records."""

    attributes = AttributeSerializer(many=True, required=False)
    workflow = WorkflowSerializer(required=False)
    pages = PageSerializer(many=True, required=False)
    owner = UserSerializer(field_set='attribute', required=False)
    creation_user = UserSerializer(field_set='attribute', required=False)
    modification_user = UserSerializer(field_set='attribute', required=False)
    image_urls = serializers.SerializerMethodField()
    collections = RecordAttributeCollectionSerializer(many=True, required=False)
    # annotated fields
    description = serializers.ReadOnlyField()
    record_type = RecordTypeSerializer()
    date = serializers.ReadOnlyField()

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
            'public': [
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
            'images': ['image_urls'],
        }

    def get_image_urls(self, obj):
        try:
            img_id = obj.pages.exclude(dam_id__isnull=True).first().dam_id
            return rs_resource.objects.get(ref=img_id).get_image_url('scr,thm')
        except (KeyError, ValueError):
            return None
