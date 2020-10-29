from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from dalme_app.utils import DALMEMenus as dm
from dalme_app.models import Ticket
from django.core.exceptions import ObjectDoesNotExist
from ._common import DALMEListView, get_page_chain
from django.conf import settings


@method_decorator(login_required, name='dispatch')
class TicketDetail(DetailView):
    model = Ticket
    template_name = 'dalme_app/ticket_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['api_endpoint']: settings.API_ENDPOINT
        breadcrumb = [('Project', ''), ('Issue Tickets', '/tickets')]
        sidebar_toggle = self.request.user.preferences['interface__sidebar_collapsed']
        context['sidebar_toggle'] = sidebar_toggle
        state = {'breadcrumb': breadcrumb, 'sidebar': sidebar_toggle}
        context['dropdowns'] = dm(self.request, state).dropdowns
        context['sidebar'] = dm(self.request, state).sidebar
        page_title = 'Ticket #'+str(self.object.id)
        context['page_title'] = page_title
        context['page_chain'] = get_page_chain(breadcrumb, page_title)
        context['ticket'] = self.object
        return context

    def get_object(self):
        try:
            object = super().get_object()
            return object
        except ObjectDoesNotExist:
            raise Http404


@method_decorator(login_required, name='dispatch')
class TicketList(DALMEListView):
    page_title = 'Issue Tickets'
    dt_config = 'tickets'
    breadcrumb = [('Project', ''), ('Issue Tickets', '/tickets')]
