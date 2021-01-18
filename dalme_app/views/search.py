import json
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from ._common import DALMEContextMixin
from dalme_app.utils import Search, formset_factory, SearchContext
from dalme_app.forms import SearchForm
from django.shortcuts import render
from datetime import datetime, timedelta
from dalme_app.models import SavedSearch


@method_decorator(login_required, name='dispatch')
class DefaultSearch(TemplateView, DALMEContextMixin):
    template_name = 'dalme_app/search.html'
    breadcrumb = [('Search', ''), ('Search', '')]
    page_title = 'Search'
    search_context = SearchContext(public=False)
    search_formset = formset_factory(SearchForm)

    def dispatch(self, request, *args, **kwargs):
        if not request.method == 'POST' and request.session.get('search-post', False):
            default_ts = datetime.timestamp(datetime.now() - timedelta(seconds=86401))
            stored_dt = datetime.fromtimestamp(request.session.get('search-ts', default_ts))
            delta = datetime.now() - stored_dt
            if delta.seconds < 86400:
                request.POST = request.session['search-post']
                request.method = 'POST'

        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed

        return handler(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'query': False,
            'advanced': False,
            'form': self.search_formset(form_kwargs={'fields': self.search_context.fields}),
            'results': [],
            'paginator': {},
            'errors': False,
            'paginated': False,
            'suggestion': None,
            'search': True,
            'search_context': self.search_context.context
        })
        return context

    def post(self, request, **kwargs):
        formset = self.search_formset(request.POST, form_kwargs={'fields': self.search_context.fields})
        clean_request = request.POST.copy()
        clean_request['form-SAVE'] = None
        request.session['search-post'] = clean_request
        request.session['search-ts'] = datetime.timestamp(datetime.now())
        context = self.get_context_data(**kwargs)
        if formset.is_valid():
            search_obj = Search(
                data=formset.cleaned_data,
                page=request.POST.get('form-PAGE', 1),
                highlight=True,
                search_context=self.search_context.context
            )

            success = None
            if request.POST.get('form-SAVE'):
                success = self.save_search(request)

            context.update({
                'query': True,
                'advanced': formset.cleaned_data[0].get('field_value', '') != '',
                'form': formset,
                'results': search_obj.results,
                'paginator': search_obj.paginator,
                'errors': search_obj.errors,
                'success': success,
                'paginated': search_obj.paginator.get('num_pages', 0) > 1
            })

        return render(request, self.template_name, context)

    def save_search(self, request):
        try:
            search = SavedSearch()
            search.name = request.POST['form-SAVE']
            search.search = json.dumps(request.POST)
            search.owner = request.user
            search.save()
            return 'Search saved succesfully.'

        except Exception as e:
            return f'Error saving search: {str(e)}'
