from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from ._common import DALMEContextMixin
from dalme_app import custom_scripts


@method_decorator(login_required, name='dispatch')
class Scripts(TemplateView, DALMEContextMixin):
    template_name = 'dalme_app/scripts.html'
    breadcrumb = [('Tools', ''), ('Scripts', '/scripts')]
    page_title = 'Custom Scripts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['scripts'] = custom_scripts.get_script_menu()
        if self.request.GET.get('s') is not None:
            context['output'] = eval('custom_scripts.'+self.request.GET['s']+'(self.request)')
        return context
