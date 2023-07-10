from collections import OrderedDict
from contextlib import suppress

from rest_framework.pagination import LimitOffsetPagination, _positive_int
from rest_framework.response import Response


class DALMELimitOffsetPagination(LimitOffsetPagination):
    """Subclasses LimitOffsetPagination to add metadata to response if requested."""

    filtered_count = None
    context = None

    def paginate_queryset(self, queryset, request, view=None):
        """Paginate the passed queryset."""
        self.limit = self.get_limit(request)
        self.count = self.get_count(queryset)
        self.filtered_count = self.count
        self.offset = self.get_offset(request)
        self.request = request

        if view and hasattr(view, 'context'):
            self.context = view.context

        if self.limit in [None, 0] or self.limit > self.count:
            return list(queryset)

        if self.count == 0 or self.offset > self.count:
            return []

        if self.count > self.limit and self.template is not None:
            self.display_page_controls = True

        queryset = queryset[self.offset : self.offset + self.limit]
        self.filtered_count = self.get_count(queryset)

        return list(queryset)

    def get_paginated_response(self, data_object):
        """Return paginated response object."""
        # try:
        #     data, queryset, instance = data_object
        # except ValueError:
        #     data, queryset, instance = data_object, None, None

        # if not isinstance(data, list):
        #     data = [data]

        # response_obj = [
        #     ('count', self.count),
        #     ('filtered', self.filtered_count),
        #     ('data', data),
        # ]

        response_obj = [
            ('count', self.count),
            ('filtered', self.filtered_count),
            ('data', data_object),
        ]

        if self.context:
            for key, value in self.context.items():
                response_obj.append((key, value))

        # if self.request.GET.get('meta') is not None and instance is not None:
        #     response_obj.append(('meta', instance.get_metadata(queryset)))

        return Response(OrderedDict(response_obj))

    def get_limit(self, request):
        """Return page limit."""
        if self.limit_query_param:
            with suppress(KeyError, ValueError):
                return _positive_int(request.query_params[self.limit_query_param], strict=False, cutoff=self.max_limit)

        return self.default_limit
