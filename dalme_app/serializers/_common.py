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
