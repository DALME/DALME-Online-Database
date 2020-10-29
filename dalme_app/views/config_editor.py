from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.conf import settings
from dalme_app.utils import DALMEMenus as dm
from ._common import get_page_chain


@method_decorator(login_required, name='dispatch')
class ConfigEditor(TemplateView):
    template_name = 'dalme_app/config_editor.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breadcrumb = [('Tools', ''), ('Config Editor', '/config-editor')]
        sidebar_toggle = self.request.user.preferences['interface__sidebar_collapsed']
        state = {
            'breadcrumb': breadcrumb,
            'sidebar': sidebar_toggle
        }
        page_title = 'Config Editor'

        context.update({
            'api_endpoint': settings.API_ENDPOINT,
            'sidebar_toggle': sidebar_toggle,
            'dropdowns': dm(self.request, state).dropdowns,
            'sidebar': dm(self.request, state).sidebar,
            'page_title': page_title,
            'page_chain': get_page_chain(breadcrumb, page_title)
        })

        return context
