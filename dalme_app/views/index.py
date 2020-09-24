from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from dalme_app.utils import DALMEMenus as dm
from ._common import get_page_chain
from django.views.generic.base import TemplateView


@method_decorator(login_required, name='dispatch')
class Index(TemplateView):
    template_name = 'dalme_app/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breadcrumb = [('Dashboard', '')]
        sidebar_toggle = self.request.user.preferences['interface__sidebar_collapsed']
        self.request.session['sidebar_toggle'] = sidebar_toggle
        state = {'breadcrumb': breadcrumb, 'sidebar': sidebar_toggle}
        context['sidebar_toggle'] = sidebar_toggle
        context['dropdowns'] = dm(self.request, state).dropdowns
        context['sidebar'] = dm(self.request, state).sidebar
        page_title = 'Dashboard'
        context['page_title'] = page_title
        context['page_chain'] = get_page_chain(breadcrumb, page_title)
        context['cards'] = self.request.user.preferences['interface__homepage_cards']
        return context
