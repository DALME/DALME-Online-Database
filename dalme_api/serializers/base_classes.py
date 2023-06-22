from rest_framework import serializers

from dalme_app.models import Workflow


class DynamicSerializer(serializers.ModelSerializer):
    """A serializer that takes an additional `fields` argument that indicates which fields should be included."""

    def __init__(self, *args, **kwargs):  # noqa: D107
        if 'fields' in kwargs and 'field_set' in kwargs:
            msg = '`fields` and `field_set` cannot be used concurrently.'
            raise AssertionError(msg)

        fields = kwargs.pop('fields', None)
        field_set = kwargs.pop('field_set', None)
        super().__init__(*args, **kwargs)

        if field_set is not None:
            assert hasattr(self.Meta, 'field_sets'), (
                'Use of `field_set` requires the `field_sets` dictionary to be defined in the class `Meta`.',
            )
            fields = self.Meta.field_sets.get(field_set)

        if fields is not None:
            set_fields = dict(self.fields)
            for k, _v in set_fields.items():
                if k not in fields:
                    self.fields.pop(k)


def translate_workflow_string(data):
    """Return a normalized version of the workflow status string."""
    stage_by_no = dict(Workflow.PROCESSING_STAGES)
    status_by_no = dict(Workflow.WORKFLOW_STATUS)
    stage_by_name = {label: number for number, label in stage_by_no.items()}
    status_by_name = {label: number for number, label in status_by_no.items()}

    if type(data) is str:
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
