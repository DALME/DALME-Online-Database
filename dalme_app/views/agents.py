from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from ._common import DALMEListView


@method_decorator(login_required, name='dispatch')
class AgentList(DALMEListView):
    page_title = 'Agents'
    dt_config = 'agents'
    breadcrumb = [('Entities', ''), ('Agents', '/agents')]
