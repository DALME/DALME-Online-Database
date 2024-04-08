"""Records API endpoint."""

from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from wagtail.api.v2.views import BaseAPIViewSet

from django.urls import path

from ida.models import Record
from ida.utils import Search, SearchContext
from public.filters import RecordFilter
from public.pagination import PublicPagination
from public.serializers import RecordSerializer


class RecordsAPIViewSet(BaseAPIViewSet):
    base_serializer_class = RecordSerializer
    name = 'records'
    model = Record
    queryset = Record.objects.filter(workflow__is_public=True)
    lookup_url_kwarg = 'pk'
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PublicPagination
    filterset_class = RecordFilter
    meta_fields = []

    def get_serializer_class(self):
        return self.base_serializer_class

    @classmethod
    def get_urlpatterns(cls):
        return [
            path('', cls.as_view({'get': 'listing_view'}), name='listing'),
            path('<uuid:pk>/', cls.as_view({'get': 'detail_view'}), name='detail'),
            path('find/', cls.as_view({'get': 'find_view'}), name='find'),
        ]

    def listing_view(self, request):  # noqa: ARG002
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def detail_view(self, request, pk):  # noqa: ARG002
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_queryset(self):
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
            qs = self.queryset.order_by('name')
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
