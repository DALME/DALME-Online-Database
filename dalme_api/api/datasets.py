from rest_framework import viewsets
from rest_framework.response import Response
from dalme_api.access_policies import PublicAccessPolicy
from dalme_app.models import Attribute, LocaleReference
import math


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
    records = {}
    for i in source_locales:
        locale = LocaleReference.objects.filter(id=int(i.value_JSON['id']))
        if locale.exists():
            place = locale.first()
            if place.name in records:
                records[place.name]['count'] += 1
                records[place.name]['records'] += 1
            else:
                records[place.name] = {
                    'count': 1,
                    'records': 1,
                    'administrative_region': place.administrative_region,
                    'country': place.country.name,
                    'latitude': place.latitude,
                    'longitude': place.longitude
                }

    # values = [v['count'] for k, v in records.items()]
    # min_value = min(values)
    # max_value = max(values)
    # graph_min = 5
    # graph_max = 20

    for loc, data in records.items():
        # https://www.tandfonline.com/doi/pdf/10.1080/02786829608965365
        # count = data['count'] + (1 - data['count'] / 2) ** 2 if data['count'] < 5 else data['count']
        # visual range from 5px to 17px
        data['count'] = math.log(data['count']) * 2
        # data['count'] = (((data['count'] - min_value) * (graph_max - graph_min)) / (max_value - min_value)) + graph_min

    return records
