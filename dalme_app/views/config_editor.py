from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from ._common import DALMEContextMixin


@method_decorator(login_required, name='dispatch')
class ConfigEditor(TemplateView, DALMEContextMixin):
    template_name = 'dalme_app/config_editor.html'
    breadcrumb = [('Tools', ''), ('Config Editor', '/config-editor')]
    page_title = 'Config Editor'
