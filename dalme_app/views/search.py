from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from ._common import DALMEContextMixin
from dalme_app.forms import SearchForm
from django.forms import formset_factory
from dalme_app.utils import Search, SearchContext
from django.shortcuts import render


@method_decorator(login_required, name='dispatch')
class DefaultSearch(TemplateView, DALMEContextMixin):
    template_name = 'dalme_app/search.html'
    breadcrumb = [('Search', ''), ('Search', '')]
    page_title = 'Search'
    search_context = SearchContext(public=False)
    search_formset = formset_factory(SearchForm)

    def dispatch(self, request, *args, **kwargs):
        if not request.method == 'POST' and request.session.get('search-post', False):
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
        request.session['search-post'] = request.POST
        context = self.get_context_data(**kwargs)
        if formset.is_valid():
            search_obj = Search(
                data=formset.cleaned_data,
                page=request.POST.get('form-PAGE', 1),
                highlight=True,
                search_context=self.search_context.context
            )
            context.update({
                'query': True,
                'advanced': formset.cleaned_data[0].get('field_value', '') != '',
                'form': formset,
                'results': search_obj.results,
                'paginator': search_obj.paginator,
                'errors': search_obj.errors,
                'paginated': search_obj.paginator.get('num_pages', 0) > 1
            })

        return render(request, self.template_name, context)
