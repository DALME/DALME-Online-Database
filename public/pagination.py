"""Pagination for public website."""

from rest_framework import pagination
from rest_framework.response import Response

from django.core.paginator import InvalidPage


class PublicPagination(pagination.PageNumberPagination):
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
        start_page = (
            max(current_page - adjacent_pages, 1) if max(current_page - adjacent_pages, 1) >= 3 else 1  # noqa: PLR2004
        )
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
