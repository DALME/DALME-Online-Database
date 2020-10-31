from rest_framework import viewsets
from rest_framework.response import Response
from dalme_api.access_policies import PublicAccessPolicy
from dalme_app.models import Attribute, LocaleReference


class Datasets(viewsets.GenericViewSet):
    """ API endpoint for generating and retrieving DALME datasets """
    permission_classes = (PublicAccessPolicy,)

    def retrieve(self, request, pk=None, format=None):
        if pk:
            try:
                result = eval(f'{pk}()')
                status = 201
            except Exception as e:
                result = {'error': 'The following error occured while trying to get the dataset: ' + str(e)}
                status = 400
        else:
            result = {'error': 'There was no dataset id in the request.'}
            status = 400

        return Response(result, status)


def explore_map():
    source_locales = Attribute.objects.filter(attribute_type=36, sources__workflow__is_public=True)
    result = {}
    for i in source_locales:
        locale = LocaleReference.objects.filter(id=int(i.value_JSON['id']))
        if locale.exists():
            place = locale.first()
            if place.name in result:
                result[place.name]['count'] = result[place.name]['count'] + 1
            else:
                result[place.name] = {
                    'count': 1,
                    'administrative_region': place.administrative_region,
                    'country': place.country.name,
                    'latitude': place.latitude,
                    'longitude': place.longitude
                }

    return result
