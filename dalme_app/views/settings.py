from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormMixin
from django.views.generic.base import TemplateView
from ._common import DALMEContextMixin
from dalme_app.forms import preference_form_builder
from dalme_app.forms import GlobalPreferenceForm


@method_decorator(login_required, name='dispatch')
class Settings(FormMixin, TemplateView, DALMEContextMixin):
    template_name = 'dalme_app/settings.html'
    form_class = GlobalPreferenceForm
    breadcrumb = [('Tools', ''), ('Settings', '/settings')]
    page_title = 'Settings'

    def get_form_class(self, *args, **kwargs):
        form_class = preference_form_builder(self.form_class)
        return form_class

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form': self.get_form(),
            'section_list': [i[0] for i in self.form_class.registry.section_objects.items()]
        })
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
