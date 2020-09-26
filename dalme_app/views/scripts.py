from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from dalme_app.utils import DALMEMenus as dm
from ._common import get_page_chain
from dalme_app import custom_scripts


@method_decorator(login_required, name='dispatch')
class Scripts(TemplateView):
    template_name = 'dalme_app/scripts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breadcrumb = [('Tools', ''), ('Scripts', '/scripts')]
        sidebar_toggle = self.request.user.preferences['interface__sidebar_collapsed']
        state = {'breadcrumb': breadcrumb, 'sidebar': sidebar_toggle}
        context['sidebar_toggle'] = sidebar_toggle
        context['dropdowns'] = dm(self.request, state).dropdowns
        context['sidebar'] = dm(self.request, state).sidebar
        context['scripts'] = custom_scripts.get_script_menu()
        page_title = 'Custom Scripts'
        context['page_title'] = page_title
        context['page_chain'] = get_page_chain(breadcrumb, page_title)
        if self.request.GET.get('s') is not None:
            context['output'] = eval('custom_scripts.'+self.request.GET['s']+'(self.request)')
        return context
