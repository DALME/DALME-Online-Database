"""API endpoint for managing datasets."""

import numpy as np
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from rest_framework import viewsets
from rest_framework.response import Response

from api.access_policies import PublicAccessPolicy
from ida.models import Record


class Datasets(viewsets.GenericViewSet):
    """API endpoint for generating and retrieving datasets."""

    permission_classes = [PublicAccessPolicy]
    oauth_permission_classes = [TokenHasReadWriteScope]

    def retrieve(self, request, pk=None, fmt=None):  # noqa: ARG002
        """Return requested dataset."""
        if pk is None:
            return Response({'error': 'There was no dataset id in the request.'}, 400)

        try:
            return Response(eval(f'self.{pk}()'), 201)

        except Exception as e:  # noqa: BLE001
            return Response({'error': str(e)}, 400)

    def explore_map(self):
        """Return data for 'Explore' map in public site."""
        records = (
            Record.objects.include_attrs('locale')
            .filter(workflow__is_public=True)
            .prefetch_related(
                'attributes',
                'collections',
                'collections__collection',
            )
        )
        place_data = {}
        for record in records:
            date = record.get_date()
            years = date.year if date else []
            years = years if isinstance(years, list) else [years]
            collections = [c.collection.name for c in record.collections.filter(collection__is_published=True)]
            if record.locale:
                locales = record.locale if isinstance(record.locale, list) else [record.locale]
                for loc in locales:
                    if loc.name in place_data:
                        place_data[loc.name]['count'] += 1
                        place_data[loc.name]['coverage'] += years
                        place_data[loc.name]['collections'] += collections
                    else:
                        place_data[loc.name] = {
                            'locale_id': loc.id,
                            'count': 1,
                            'administrative_region': loc.administrative_region,
                            'country': loc.country.name,
                            'latitude': loc.latitude,
                            'longitude': loc.longitude,
                            'coverage': years if years else [],
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
