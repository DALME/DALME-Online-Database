from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from ._common import DALMEContextMixin
from dalme_app.forms import SearchForm
from dalme_app.documents import SourceDocument


@method_decorator(login_required, name='dispatch')
class DefaultSearch(TemplateView, DALMEContextMixin):
    template_name = 'dalme_app/search.html'
    searchindex = SourceDocument()
    query = ''
    breadcrumb = [('Search', ''), ('Search', '')]
    page_title = 'Search'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        (paginator, results) = self.get_results()
        context.update({
            'form': SearchForm(),
            'paginator': paginator,
            'results': results,
            'query': self.query,
            'paginated': paginator.get('num_pages', 0) > 1,
        })

        return context

    def get_results(self):
        paginator = {}
        results = []

        if self.request.GET.get('q') is not None:
            form = SearchForm(self.request.GET)
            if form.is_valid():
                self.query = form.cleaned_data['q']
                (paginator, results) = form.search(
                    searchindex=self.searchindex,
                    page=self.request.GET.get('page', 1),
                    highlight=('text', {
                        'fragment_size': 100
                        })
                )

        return paginator, results
