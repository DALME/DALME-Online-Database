from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from dalme_api.access_policies import SessionAccessPolicy


class Session(viewsets.ViewSet):
    """ API endpoint for managing user sessions """
    permission_classes = (SessionAccessPolicy,)

    @action(detail=False, methods=['post'])
    def alter(self, request):

        if request.data is not None:
            result = []
            for key, value in request.data.items():
                if not value:
                    try:
                        del request.session[key]
                        result.append({'key': key, 'result': 'deleted'})
                    except KeyError:
                        result.append({'key': key, 'result': 'skipped - does not exist'})
                else:
                    request.session[key] = value
                    result.append({'key': key, 'result': f'new value: {value}'})

            status = 201

        else:
            result = {'error': 'Data missing from request.'}
            status = 400

        return Response(result, status)
