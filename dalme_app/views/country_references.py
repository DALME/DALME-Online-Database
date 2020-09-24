from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from ._common import DALMEListView


@method_decorator(login_required, name='dispatch')
class CountryList(DALMEListView):
    page_title = 'Countries'
    dt_config = 'countries'
    breadcrumb = [('System', ''), ('Countries', '/countries')]
