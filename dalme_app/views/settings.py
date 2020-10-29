from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormMixin
from django.views.generic.base import TemplateView
from dalme_app.utils import DALMEMenus as dm
from ._common import get_page_chain
from dalme_app.forms import preference_form_builder
from dalme_app.forms import GlobalPreferenceForm
from django.conf import settings


@method_decorator(login_required, name='dispatch')
class Settings(FormMixin, TemplateView):
    template_name = 'dalme_app/settings.html'
    form_class = GlobalPreferenceForm

    def get_form_class(self, *args, **kwargs):
        form_class = preference_form_builder(self.form_class)
        return form_class

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['api_endpoint']: settings.API_ENDPOINT
        breadcrumb = [('Tools', ''), ('Settings', '/settings')]
        sidebar_toggle = self.request.user.preferences['interface__sidebar_collapsed']
        state = {'breadcrumb': breadcrumb, 'sidebar': sidebar_toggle}
        context['sidebar_toggle'] = sidebar_toggle
        context['dropdowns'] = dm(self.request, state).dropdowns
        context['sidebar'] = dm(self.request, state).sidebar
        page_title = 'Settings'
        context['page_title'] = page_title
        context['page_chain'] = get_page_chain(breadcrumb, page_title)
        context['form'] = self.get_form()
        context['section_list'] = [i[0] for i in self.form_class.registry.section_objects.items()]
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return self.request.path

    def form_valid(self, form):
        form.update_preferences()
        return super(Settings, self).form_valid(form)
