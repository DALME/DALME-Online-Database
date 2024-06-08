"""Model search-enabled page data."""

import contextlib
import json
from datetime import datetime, timedelta

from wagtail.contrib.routable_page.models import RoutablePageMixin, path

from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.utils import timezone

from ida.forms import SearchForm
from ida.models import Record, SavedSearch
from ida.utils import Search, SearchContext, formset_factory
from public.models.base_page import BasePage
from public.models.settings import Settings


class SearchEnabled(RoutablePageMixin, BasePage):
    metadata_panels = BasePage.metadata_panels

    class Meta:
        abstract = True

    @path('search/', name='search')
    @path('search/<uuid:pk>/', name='saved_search')
    def search(self, request, pk=None):
        context = self.get_context(request)
        search_context = SearchContext(public=True)
        search_formset = formset_factory(SearchForm)

        context.update(
            {
                'header_image': Settings.objects.first().search_header_image,
                'header_position': Settings.objects.first().search_header_position,
                'query': False,
                'advanced': False,
                'form': search_formset(form_kwargs={'fields': search_context.fields}),
                'results': [],
                'paginator': {},
                'errors': False,
                'paginated': False,
                'suggestion': None,
                'search': True,
                'search_context': search_context.context,
            },
        )

        if pk:
            saved_search = SavedSearch.objects.filter(id=pk)
            if saved_search.exists():
                saved_search = json.loads(saved_search.first().search)
                saved_search.pop('csrfmiddlewaretoken')
                saved_search['form-SAVE'] = ''
                request.POST = saved_search
                request.method = 'POST'

        if request.method != 'POST' and request.session.get('public-search-post', False):
            seconds = 86401
            default_ts = datetime.timestamp(
                datetime.now(tz=timezone.get_current_timezone()) - timedelta(seconds=seconds),
            )
            stored_dt = datetime.fromtimestamp(
                request.session.get('public-search-ts', default_ts),
                tz=timezone.get_current_timezone(),
            )
            delta = datetime.now(tz=timezone.get_current_timezone()) - stored_dt
            if delta.seconds < seconds:
                request.POST = request.session['public-search-post']
                request.method = 'POST'

        if request.method == 'POST':
            formset = search_formset(request.POST, form_kwargs={'fields': search_context.fields})
            request.session['public-search-post'] = request.POST
            request.session['public-search-ts'] = datetime.timestamp(
                datetime.now(tz=timezone.get_current_timezone()),
            )
            if formset.is_valid():
                search_obj = Search(
                    data=formset.cleaned_data,
                    public=True,
                    page=request.POST.get('form-PAGE', 1),
                    highlight=True,
                    search_context=search_context.context,
                )
                context.update(
                    {
                        'query': True,
                        'advanced': formset.cleaned_data[0].get('field_value', '') != '',
                        'form': formset,
                        'results': search_obj.results,
                        'paginator': search_obj.paginator,
                        'errors': search_obj.errors,
                        'paginated': search_obj.paginator.get('num_pages', 0) > 1,
                    },
                )

        return render(
            request,
            'public/search.html',
            context,
        )

    @path('records/', name='records')
    def records(self, request, scoped=True):  # noqa: ARG002
        context = self.get_context(request)

        context.update(
            {
                'header_image': Settings.objects.first().browser_header_image,
                'header_position': Settings.objects.first().browser_header_position,
                'records': True,
                'browse_mode': request.session.get('public-browse-mode', 'wide'),
            },
        )

        with contextlib.suppress(AttributeError):
            context.update({'collection_id': self.record_collection.id})

        return TemplateResponse(
            request,
            'public/records.html',
            context,
        )

    @path('records/<uuid:pk>/', name='record')
    @path('records/<uuid:pk>/<str:folio>/', name='record_folio')
    def record(self, request, pk, folio=None, scoped=True):  # noqa: ARG002
        qs = Record.objects.include_attrs('record_type', 'description', 'locale', 'language').filter(pk=pk)
        if not qs.exists():
            raise Http404

        record = qs.first()
        as_preview = self.preview if hasattr(self, 'preview') else False

        if not record.workflow.is_public and not as_preview:
            raise Http404

        pages = [
            {
                'pageId': i.id,
                'pageName': i.name,
                'transcriptionId': i.transcription.id,
                'pageOrder': i.order,
                'pageImageId': i.dam_id,
            }
            for i in record.pages.all().order_by('order')
        ]

        initial_folio_index = (
            next(
                (i for i, item in enumerate(pages) if item['pageName'] == folio),
                0,
            )
            if folio
            else 0
        )

        context = self.get_context(request)

        from_search = False
        if request.META.get('HTTP_REFERER') and 'search' in request.META.get('HTTP_REFERER'):
            from_search = True

        # import serializer here to avoid exception if api is not yet loaded
        from api.resources.records.serializers import RecordSerializer

        data = RecordSerializer(record, field_set=['public', 'public_detail']).data
        purl = f'{settings.BASE_URL}/purl/{record.id}/' if as_preview else record.get_purl()

        context.update(
            {
                'header_image': Settings.objects.first().viewer_header_image,
                'header_position': Settings.objects.first().viewer_header_position,
                'record': True,
                'from_search': from_search,
                'viewer_mode': request.session.get('public-viewer-mode', 'vertical-split'),
                'render_mode': request.session.get('public-render-mode', 'scholarly'),
                'purl': purl,
                'title': self.smart_truncate(data['name'], length=35),
                'data': {
                    'folios': list(pages),
                    **data,
                },
                'initial_folio_index': initial_folio_index,
            },
        )

        with contextlib.suppress(AttributeError):
            context.update({'collection_id': self.record_collection.id})

        return TemplateResponse(
            request,
            'public/record.html',
            context,
        )

    def relative_url(self, current_site, request=None):
        if hasattr(request, 'is_dummy') and request.is_dummy:
            return '/'
        return self.get_url(request=request, current_site=current_site)
