from rest_framework.pagination import LimitOffsetPagination, _positive_int
from rest_framework.response import Response
from collections import OrderedDict


class DALMELimitOffsetPagination(LimitOffsetPagination):
    """ Subclasses LimitOffsetPagination to add metadata to
    response if requested """

    total_count = None

    def paginate_queryset(self, queryset, request, view=None):
        self.limit = self.get_limit(request)
        self.total_count = self.get_count(queryset)
        self.count = self.get_count(queryset)
        self.offset = self.get_offset(request)
        self.request = request
        if self.limit in [None, 0]:
            return list(queryset)

        if self.count > self.limit and self.template is not None:
            self.display_page_controls = True

        if self.count == 0 or self.offset > self.count:
            return []

        return list(queryset[self.offset:self.offset + self.limit])

    def get_paginated_response(self, data_object):
        try:
            data, queryset, instance = data_object
        except ValueError:
            data, queryset, instance = data_object, None, None

        if not isinstance(data, list):
            data = [data]

        response_obj = [
            ('recordsFiltered', self.count),
            ('recordsTotal', self.total_count),
            ('data', data)
        ]

        if self.request.GET.get('meta') is not None and instance is not None:
            response_obj.append(('meta', instance.get_metadata(queryset)))

        return Response(OrderedDict(response_obj))

    def get_limit(self, request):
        if self.limit_query_param:
            try:
                return _positive_int(
                    request.query_params[self.limit_query_param],
                    strict=False,
                    cutoff=self.max_limit
                )
            except (KeyError, ValueError):
                pass

        return self.default_limit
