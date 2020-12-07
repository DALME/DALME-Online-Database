from rest_framework import viewsets
from rest_framework.response import Response
from dalme_api.access_policies import PublicAccessPolicy
from dalme_app.models import LocaleReference, Source
import numpy as np


class Datasets(viewsets.GenericViewSet):
    """ API endpoint for generating and retrieving DALME datasets """
    permission_classes = (PublicAccessPolicy,)

    def retrieve(self, request, pk=None, format=None):
        if pk:
            try:
                result = eval(f'self.{pk}()')
                status = 201
            except Exception as e:
                result = {'error': 'The following error occured while trying to get the dataset: ' + str(e)}
                status = 400
        else:
            result = {'error': 'There was no dataset id in the request.'}
            status = 400

        return Response(result, status)

    def explore_map(self):
        sources = Source.objects.filter(type=13, workflow__is_public=True).prefetch_related(
            'attributes', 'attributes__attribute_type', 'sets', 'sets__set_id'
        )
        place_data = {}
        for source in sources:
            source_date = list(source.attributes.filter(attribute_type__in=[19, 26]).values_list('value_DATE_y', flat=True))
            source_collections = [c.set_id.name for c in source.sets.filter(set_id__set_type=2)]
            locales = source.attributes.filter(attribute_type=36)
            if locales.exists():
                for i in locales:
                    locale = LocaleReference.objects.filter(id=int(i.value_JSON['id']))
                    if locale.exists():
                        place = locale.first()
                        if place.name in place_data:
                            place_data[place.name]['count'] += 1
                            place_data[place.name]['coverage'] += source_date
                            place_data[place.name]['collections'] += source_collections
                        else:
                            place_data[place.name] = {
                                'locale_id': place.id,
                                'count': 1,
                                'administrative_region': place.administrative_region,
                                'country': place.country.name,
                                'latitude': place.latitude,
                                'longitude': place.longitude,
                                'coverage': source_date,
                                'collections': source_collections,
                            }
        # CLASSIFICATION:
        # we need to classify the values we want to show on the map as neither a linear nor log scales look good otherwise.
        # the parameters were determined visually: the smallest possible circle is 3px in radius (otherwise they are hard to see)
        # the largest that's okay is about 19px. Size differences of less than 2px (radius, i.e 4 in diametre) are imperceptible
        # so that gives us 9 sizes between 3px and 19px in increments of 2px.
        # Process:
        values = [v['count'] for k, v in place_data.items()]  # get the list of all values in the sample
        bins = np.geomspace(min(values), max(values), 9)  # create 9 bins using a geometric progression, instead of logarithmic so that each point is a constant multiple of the previous one
        freq, bins = np.histogram(values, bins)  # classify using histogram
        bin_index = np.digitize(values, bins)  # build an index — this works because numpy's bins are open on the upper limit (except the last one)
        # now we iterate over the results and assign a radius which is the (bin index * 2 ) + 1 (see explanation above)
        dataset = []
        for loc, data in place_data.items():
            dates = list(set(data.pop('coverage', [])))
            dates = dates if len(dates) > 0 else ['N/A']
            collections = list(set(data.pop('collections', [])))
            data.update({
                'name': loc,
                'records': data['count'],
                'coverage': f'{min(dates)}–{max(dates)}' if len(dates) > 1 else dates[0],
                'collections': collections,
            })
            data['count'] = (bin_index[values.index(data['count'])] * 2) + 1
            dataset.append(data)

        return sorted(dataset, key=lambda k: k['count'], reverse=True)
