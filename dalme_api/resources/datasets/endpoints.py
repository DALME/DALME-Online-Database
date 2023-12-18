"""API endpoint for managing datasets."""
import numpy as np
from rest_framework import viewsets
from rest_framework.response import Response

from dalme_api.access_policies import BaseAccessPolicy
from ida.models import Record


class PublicAccessPolicy(BaseAccessPolicy):
    """Access policies for public site."""

    id = 'public-policy'  # noqa: A003


class Datasets(viewsets.GenericViewSet):
    """API endpoint for generating and retrieving DALME datasets."""

    permission_classes = (PublicAccessPolicy,)

    def retrieve(self, request, pk=None, fmt=None):  # noqa: ARG002
        """Return requested dataset."""
        if pk is None:
            return Response({'error': 'There was no dataset id in the request.'}, 400)

        try:
            return Response(eval(f'self.{pk}()'), 201)  # noqa: PGH001

        except Exception as e:  # noqa: BLE001
            return Response({'error': str(e)}, 400)

    def explore_map(self):
        """Return data for 'Explore' map in public site."""
        records = Record.objects.filter(workflow__is_public=True).prefetch_related(
            'attributes',
            'collections',
            'collections__collection',
        )
        place_data = {}
        for record in records:
            years = list(
                record.attributes.filter(attribute_type__in=[19, 26]).values_list(
                    'attributevaluedate__year',
                    flat=True,
                ),
            )
            collections = [c.collection.name for c in record.collections.filter(collection__is_published=True)]
            locales = record.attributes.filter(attribute_type=36)
            if locales.exists():
                for loc in locales:
                    if loc.value.name in place_data:
                        place_data[loc.value.name]['count'] += 1
                        place_data[loc.value.name]['coverage'] += years
                        place_data[loc.value.name]['collections'] += collections
                    else:
                        place_data[loc.value.name] = {
                            'locale_id': loc.value.id,
                            'count': 1,
                            'administrative_region': loc.value.administrative_region,
                            'country': loc.value.country.name,
                            'latitude': loc.value.latitude,
                            'longitude': loc.value.longitude,
                            'coverage': years,
                            'collections': collections,
                        }

        # CLASSIFICATION:
        # We need to classify the values we want to show on the map as neither
        # a linear nor log scales look good otherwise. The parameters were
        # determined visually: the smallest possible circle is 3px in radius
        # (otherwise they are hard to see). The largest that's okay is about
        # 19px. Size differences of less than 2px (radius, i.e 4 in diametre)
        # are imperceptible, so that gives us 9 sizes between 3px and 19px in
        # increments of 2px.

        # Get the list of all values in the sample.
        values = [v['count'] for k, v in place_data.items()]

        # Create 9 bins using a geometric progression, instead of logarithmic
        # so that each point is a constant multiple of the previous one.
        bins = np.geomspace(min(values), max(values), 9)

        # Classify the bins with a histogram.
        _, bins = np.histogram(values, bins)

        # Build an index — this works because numpy's bins are open on the
        # upper limit (except the last one).
        bin_index = np.digitize(values, bins)

        # Now we iterate over the results and assign a radius which is the (bin
        # index * 2 ) + 1 (see explanation above).
        dataset = []
        for loc, data in place_data.items():
            dates = list(set(data.pop('coverage', [])))
            dates = dates if len(dates) > 0 else ['N/A']
            collections = list(set(data.pop('collections', [])))
            data.update(
                {
                    'name': loc,
                    'records': data['count'],
                    'coverage': f'{min(dates)}-{max(dates)}' if len(dates) > 1 else dates[0],
                    'collections': collections,
                },
            )
            data['count'] = (bin_index[values.index(data['count'])] * 2) + 1
            dataset.append(data)

        return sorted(dataset, key=lambda k: k['count'], reverse=True)
