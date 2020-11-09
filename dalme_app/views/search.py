from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from ._common import DALMEContextMixin
from dalme_app.forms import SearchForm
from dalme_app.documents import SourceDocument
from django.forms import formset_factory
from dalme_app.utils import Search
from django.shortcuts import render


@method_decorator(login_required, name='dispatch')
class DefaultSearch(TemplateView, DALMEContextMixin):
    template_name = 'dalme_app/search.html'
    breadcrumb = [('Search', ''), ('Search', '')]
    page_title = 'Search'
    searchindex = SourceDocument()
    formset = formset_factory(SearchForm)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'query': False,
            'advanced': False,
            'form': self.formset,
            'results': [],
            'paginator': {},
            'error': False,
            'paginated': False,
            'suggestion': None,
            'search': True,
        })
        return context

    def post(self, request, **kwargs):
        formset = self.formset(request.POST)
        results = []
        paginator = {}
        error = False
        if formset.is_valid():
            es_result = Search(
                data=formset.cleaned_data,
                searchindex=self.searchindex,
                page=request.POST.get('page', 1),
                highlight=True
            )
            if type(es_result) is tuple:
                (paginator, results) = es_result
            else:
                error = es_result

            context = super().get_context_data(**kwargs)
            context.update({
                'query': True,
                'advanced': formset.cleaned_data[0]['field'] != '',
                'form': formset,
                'results': results,
                'paginator': paginator,
                'error': error,
                'paginated': paginator.get('num_pages', 0) > 1,
                'suggestion': None,
                'search': True,
            })

        return render(request, self.template_name, context)
