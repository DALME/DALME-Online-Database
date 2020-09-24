import json
import os
from rest_framework import viewsets
from rest_framework.response import Response
from dalme_app.access_policies import GeneralAccessPolicy
from dalme_app.models import *


class Choices(viewsets.ViewSet):
    """ API endpoint for generating value lists for choice fields in the UI """
    permission_classes = (GeneralAccessPolicy,)

    def list(self, request, *args, **kwargs):
        type = self.request.GET.get('type')
        field = self.request.GET.get('field')
        if type is None or field is None:
            result = {'error': 'Request has no type/field information.'}
            status = 400
        else:
            try:
                if type == 'list':
                    with open(os.path.join('dalme_app', 'config', 'value_lists', '_' + field + '.json'), 'r') as fp:
                        result = json.load(fp)
                    status = 201
                elif type == 'model':
                    para = field.split('.')
                    # global_preferences = global_preferences_registry.manager()
                    # if global_preferences['api_settings__model_select_fields'].get(para[0]) is not None:
                    #     select_fields = global_preferences['api_settings__model_select_fields'].get(para[0])
                    # else:
                    #     # select_fields = ['id', 'name']
                    #     select_fields = ['name', 'id']
                    result = [{'name': label, 'id': value} for value, label in eval('{}._meta.get_field("{}").choices'.format(para[0], para[1]))]
                    status = 201
            except Exception as e:
                result = {'error': 'The following error occured while trying to fetch the data: ' + str(e)}
                status = 400
        return Response(result, status)
