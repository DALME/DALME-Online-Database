import datetime

from django.core.paginator import InvalidPage
from django.db.models import Q, Count
from django.http import JsonResponse
from django.views import View

from rest_framework import pagination
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from dalme_app.models import Attribute, Source
from dalme_app.web_serializers import RecordSerializer
from dalme_public.filters import SourceFilter
from dalme_public.models import Corpus, Collection


class DALMEPagination(pagination.PageNumberPagination):
    def get_next_link(self):
        if not self.page.has_next():
            return None
        page_number = self.page.next_page_number()
        return page_number

    def get_previous_link(self):
        if not self.page.has_previous():
            return None
        page_number = self.page.previous_page_number()
        return page_number

    def get_paginated_response(self, data):
        return Response({
            'results': data,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'totalPages': self.page.paginator.num_pages,
            'currentPage': self.page.number,
        })

    def paginate_queryset(self, queryset, request, view=None):
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


class SourceList(ListAPIView):
    model = Source
    queryset = Source.objects.all()
    serializer_class = RecordSerializer
    pagination_class = DALMEPagination
    filterset_class = SourceFilter
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs).order_by('name')
        qs = qs.filter(
            type=13, workflow__is_public=True
        ).annotate(
            no_folios=Count('pages', filter=Q(pages__source__isnull=False))
        )

        self.filterset = self.filterset_class(self.request.GET, queryset=qs)
        qs = self.filterset.qs.distinct()

        if self.filterset.annotated:
            # Currently necessary because of the inability to eliminate dupes
            # when ordering across the Source - Attribute traversal.
            seen = set()
            filtered = []
            for source in qs:
                if source.pk not in seen:
                    filtered.append(source)
                    seen.add(source.pk)
            qs = filtered

            order_by = self.request.GET.get('order_by')
            if order_by.endswith('date'):
                maxdate = datetime.date(datetime.MAXYEAR, 1, 1)
                qs = sorted(qs, key=lambda item: item.source_date or maxdate)
            if order_by.endswith('source_type'):
                qs = sorted(qs, key=lambda item: item.source_type or '')
            if order_by.startswith('-'):
                qs.reverse()

        return qs


class SourceDetail(RetrieveAPIView):
    model = Source
    queryset = Source.objects.all()
    serializer_class = RecordSerializer
    lookup_url_kwarg = 'pk'
    permission_classes = (IsAuthenticatedOrReadOnly,)


class FilterChoices(View):
    def corpus_choices(self):
        return [
            {'id': corpus.pk, 'label': corpus.title}
            for corpus in Corpus.objects.all().order_by('title')
        ]

    def collection_choices(self):
        return [
            {'id': collection.pk, 'label': collection.title}
            for collection in Collection.objects.all().order_by('title')
        ]

    def source_type_choices(self):
        types = Attribute.objects.filter(
            attribute_type__short_name='record_type'
        ).values('value_STR').distinct()
        return sorted([
            {'id': str(idx), 'label': attr['value_STR']}
            for idx, attr in enumerate(types)
        ], key=lambda choice: choice['label'])

    @property
    def methods(self):
        return {
            'corpusChoices': self.corpus_choices,
            'collectionChoices': self.collection_choices,
            'sourceTypeChoices': self.source_type_choices,
        }

    def get_data(self):
        return {key: func() for key, func in self.methods.items()}

    def get(self, request):
        return JsonResponse(self.get_data())