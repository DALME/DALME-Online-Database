from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from dalme_app.utils import DALMEMenus as dm
from ._common import get_page_chain
from django.conf import settings
from dalme_app.forms import SearchForm
from dalme_app.documents import SourceDocument


@method_decorator(login_required, name='dispatch')
class DefaultSearch(TemplateView):
    template_name = 'dalme_app/search.html'
    searchindex = SourceDocument()
    query = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['api_endpoint']: settings.API_ENDPOINT
        breadcrumb = [('Search', ''), ('Search', '')]
        sidebar_toggle = self.request.user.preferences['interface__sidebar_collapsed']
        context['sidebar_toggle'] = sidebar_toggle
        state = {'breadcrumb': breadcrumb, 'sidebar': sidebar_toggle}
        context['dropdowns'] = dm(self.request, state).dropdowns
        context['sidebar'] = dm(self.request, state).sidebar
        page_title = 'Search'
        context['page_title'] = page_title
        context['page_chain'] = get_page_chain(breadcrumb, page_title)
        context['form'] = SearchForm()

        (paginator, results) = self.get_results()
        context['paginator'] = paginator
        context['results'] = results
        context['query'] = self.query
        context['paginated'] = paginator.get('num_pages', 0) > 1,
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
