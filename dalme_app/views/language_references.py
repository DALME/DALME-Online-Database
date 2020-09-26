from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from ._common import DALMEListView


@method_decorator(login_required, name='dispatch')
class LanguageList(DALMEListView):
    page_title = 'Languages'
    dt_config = 'languages'
    breadcrumb = [('System', ''), ('Languages', '/languages')]
    helpers = ['language_forms']
