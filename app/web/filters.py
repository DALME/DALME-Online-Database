"""Filters for web app."""

import calendar
import itertools

import django_filters

from web.models import (
    Essay,
    FeaturedInventory,
    FeaturedObject,
)


class FeaturedFilter(django_filters.FilterSet):
    @property
    def qs(self):
        qs = super().qs

        kind = self.data.get('kind')
        if kind:
            model = {
                'essay': Essay,
                'inventory': FeaturedInventory,
                'object': FeaturedObject,
            }.get(kind)
            if model:
                qs = [page for page in qs if isinstance(page, model)]

        order = self.data.get('order_by', 'date')
        if order == 'date':
            grouped = []
            qs = sorted(qs, key=lambda obj: obj.last_published_at, reverse=True)
            by_year = [
                (key, list(values))
                for key, values in itertools.groupby(
                    qs,
                    key=lambda obj: obj.last_published_at.year,
                )
            ]
            for year, values in by_year:
                by_month = [
                    (key, list(values))
                    for key, values in itertools.groupby(
                        values,
                        key=lambda obj: calendar.month_name[obj.last_published_at.month],
                    )
                ]
                grouped.append((year, by_month))
        else:
            qs = sorted(qs, key=lambda obj: obj.owner.last_name)
            grouped = [
                (key, list(values))
                for key, values in itertools.groupby(
                    qs,
                    key=lambda obj: f'{obj.byline}',
                )
            ]

        return grouped
