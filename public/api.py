"""API endpoints for public resources."""

from rest_framework import pagination
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from django.core.paginator import InvalidPage
from django.http import JsonResponse
from django.views import View

from ida.models import Record
from ida.models.resourcespace import rs_resource
from ida.utils import Search, SearchContext
from public.filters import RecordFilter, _map_record_types, locale_choices
from public.models import Collection, Corpus
from public.serializers import PublicRecordSerializer


class IDAPagination(pagination.PageNumberPagination):
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
                'page_numbers': page_numbers,
                'page_start': start_offset + 1,
                'page_end': result_end - 1 if result_end != total_count else result_end,
            },
        )


class Thumbnail(View):
    """API endpoint for returning thumbnails."""

    def get_data(self):
        """Get the thumbnail's URL."""
        try:
            thumbnail = rs_resource.objects.get(
                ref=self.request.GET['image_ref'],
            ).get_image_url(self.request.GET['size'])
        except (KeyError, ValueError):
            thumbnail = None
        return {'image_url': thumbnail}

    def get(self, request):  # noqa: ARG002
        """Return thumbnail URL."""
        return JsonResponse(self.get_data())


class RecordList(ListAPIView):
    """API endpoint for record lists."""

    model = Record
    queryset = Record.objects.filter(workflow__is_public=True)
    serializer_class = PublicRecordSerializer
    pagination_class = IDAPagination
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


class RecordDetail(RetrieveAPIView):
    """API endpoint for single record instances."""

    model = Record
    queryset = Record.objects.all()
    serializer_class = PublicRecordSerializer
    lookup_url_kwarg = 'pk'
    permission_classes = [IsAuthenticatedOrReadOnly]


class FilterChoices(View):
    """API endpoint for returning filter options."""

    def corpus_choices(self):
        """Return options for `corpus`."""
        choices = [{'value': corpus.pk, 'text': corpus.title} for corpus in Corpus.objects.all().order_by('title')]
        return [{'value': '', 'text': 'Filter by corpus', 'disabled': True}, *choices]

    def collection_choices(self):
        """Return options for `collection`."""
        choices = [
            {'value': collection.pk, 'text': collection.title}
            for collection in Collection.objects.all().order_by('title')
        ]
        return [{'value': '', 'text': 'Filter by collection', 'disabled': True}, *choices]

    def record_type_choices(self):
        """Return options for `record_type`."""
        types = _map_record_types()
        choices = sorted(
            [{'value': str(idx), 'text': value} for idx, value in types.items()],
            key=lambda choice: choice['text'],
        )
        return [{'value': '', 'text': 'Filter by record type', 'disabled': True}, *choices]

    def locale_choices_as_dict(self):
        """Return options for `locale`."""
        choices = [{'value': i[0], 'text': i[1]} for i in locale_choices()]
        return [{'value': '', 'text': 'Filter by locale', 'disabled': True}, *choices]

    @property
    def methods(self):
        """Redirect request to the appropriate method."""
        return {
            'corpusChoices': self.corpus_choices,
            'collectionChoices': self.collection_choices,
            'recordTypeChoices': self.record_type_choices,
            'localeChoices': self.locale_choices_as_dict,
        }

    def get_data(self):
        """Return the options data."""
        return {key: func() for key, func in self.methods.items()}

    def get(self, request):  # noqa: ARG002
        """Return the requested data."""
        return JsonResponse(self.get_data())
