"""Define API paginators."""

from collections import OrderedDict
from contextlib import suppress

from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination, _positive_int
from rest_framework.response import Response

from django.core.paginator import InvalidPage


class LimitOffsetPagination(LimitOffsetPagination):
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
        response_obj = [
            ('count', self.count),
            ('filtered', self.filtered_count),
            ('data', data_object),
        ]

        if self.context:
            for key, value in self.context.items():
                response_obj.append((key, value))

        return Response(OrderedDict(response_obj))

    def get_limit(self, request):
        """Return page limit."""
        if self.limit_query_param:
            with suppress(KeyError, ValueError):
                return _positive_int(
                    request.query_params[self.limit_query_param],
                    strict=False,
                    cutoff=self.max_limit,
                )

        return self.default_limit


class IDAPageNumberPagination(PageNumberPagination):
    """Pagination class for front-end."""

    page_size = 25

    def get_next_link(self):
        """Return next link."""
        if not self.page.has_next():
            return None
        return self.page.next_page_number()

    def get_previous_link(self):
        """Return previous link."""
        if not self.page.has_previous():
            return None
        return self.page.previous_page_number()

    def paginate_queryset(self, queryset, request, view=None):  # noqa: ARG002
        """Paginate the queryset."""
        page_size = self.get_page_size(request)
        if not page_size:
            return None

        paginator = self.django_paginator_class(queryset, page_size)
        page_number = request.query_params.get(self.page_query_param, 1)
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages

        try:
            self.page = paginator.page(page_number)
        except InvalidPage:
            self.page = paginator.page(1)

        if paginator.num_pages > 1 and self.template is not None:
            self.display_page_controls = True

        self.request = request
        return list(self.page)

    def get_paginated_response(self, data):
        """Return paginated `Response` object."""
        page_size = self.page_size
        current_page = self.page.number
        total_count = self.page.paginator.count
        num_pages = self.page.paginator.num_pages
        adjacent_pages = 1
        start_offset = (current_page - 1) * page_size
        result_end = start_offset + page_size + 1
        if result_end > total_count:
            result_end = total_count
        start_page = max(current_page - adjacent_pages, 1) if max(current_page - adjacent_pages, 1) >= 3 else 1  # noqa: PLR2004
        end_page = current_page + adjacent_pages if current_page + adjacent_pages <= num_pages else num_pages
        page_numbers = list(range(start_page, end_page + 1))

        return Response(
            {
                'results': data,
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'count': total_count,
                'totalPages': num_pages,
                'currentPage': current_page,
                'pageNumbers': page_numbers,
                'pageStart': start_offset + 1,
                'pageEnd': result_end - 1 if result_end != total_count else result_end,
            },
        )
