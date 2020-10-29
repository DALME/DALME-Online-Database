from rest_framework import serializers
from dalme_app.models import Workflow


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


def translate_workflow_string(data):
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

            elif status == 3:
                return {
                            'wf_status': status,
                            'stage': 5,
                            'ingestion_done': True,
                            'transcription_done': True,
                            'markup_done': True,
                            'review_done': True,
                            'parsing_done': True
                       }

        elif len(str_elements) == 2:
            stage_name = str_elements[1].strip().lower()
            stage = stage_by_name[stage_name] - 1
            value = {
                        'wf_status': 2,
                        'stage': stage
                    }

            for i in range(1, 6):
                value[stage_by_no[i] + '_done'] = True if i <= stage else False

            return value

        elif len(str_elements) == 3:
            stage_name = str_elements[0].strip().lower()
            stage = stage_by_name[stage_name]
            value = {
                        'wf_status': 2,
                        'stage': stage
                    }

            for i in range(1, 6):
                value[stage_by_no[i] + '_done'] = True if i < stage else False

            return value

        else:
            raise ValueError('Incorrect data supplied: invalid text string.')

    else:
        raise ValueError('Incorrect data supplied: must be a string.')
