from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from ._common import DALMEListView


@method_decorator(login_required, name='dispatch')
class LocaleList(DALMEListView):
    page_title = 'Locales'
    dt_config = 'locales'
    breadcrumb = [('System', ''), ('Locales', '/locales')]
