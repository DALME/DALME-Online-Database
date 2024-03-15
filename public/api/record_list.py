"""API endpoints for public resources."""

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from ida.models import Record
from ida.utils import Search, SearchContext
from public.filters import RecordFilter
from public.pagination import PublicPagination
from public.serializers import RecordSerializer


class RecordList(ListAPIView):
    """API endpoint for record lists."""

    model = Record
    queryset = Record.objects.filter(workflow__is_public=True)
    serializer_class = RecordSerializer
    pagination_class = PublicPagination
    filterset_class = RecordFilter
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):  # noqa: ARG002
        """Return list of records."""
        queryset = self.get_queryset()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self, *args, **kwargs):
        """Return the filtered queryset."""
        qs = []
        if self.request.GET.get('search'):
            search_context = SearchContext(public=True)
            search_obj = Search(
                data=[{'query': self.request.GET.get('search').strip(), 'field_value': ''}],
                public=True,
                highlight=False,
                search_context=search_context.context,
                as_queryset=True,
                sort='name',
            )
            qs = search_obj.results

        else:
            qs = super().get_queryset(*args, **kwargs).order_by('name')
            qs = qs.prefetch_related(
                'attributes',
                'attributes__attribute_type',
            )

        self.filterset = self.filterset_class(
            self.request.GET,
            queryset=qs,
        )
        qs = self.filterset.qs.distinct()

        if self.filterset.annotated:
            # Currently necessary because of the inability to eliminate
            # dupes when ordering across the Record - Attribute traversal.
            seen = set()
            filtered = []
            for record in qs:
                if record.pk not in seen:
                    filtered.append(record)
                    seen.add(record.pk)
            qs = filtered

            # Sorting by 'name' happens on the Order filter itself as we
            # are dealing with a plain qs without any annotations there.
            order_by = self.request.GET.get('order_by')
            if order_by.endswith('date'):
                qs = sorted(
                    qs,
                    key=lambda item: item.record_date or 9999,
                )
            if order_by.endswith('record_type'):
                qs = sorted(qs, key=lambda item: item.record_type or '')
            if order_by.startswith('-'):
                qs.reverse()

        return qs
