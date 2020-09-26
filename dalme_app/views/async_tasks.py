from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from ._common import DALMEListView


@method_decorator(login_required, name='dispatch')
class AsyncTaskList(DALMEListView):
    page_title = 'Asynchronous Tasks'
    dt_config = 'async_tasks'
    breadcrumb = [('System', ''), ('Asynchronous Tasks', '/async_tasks')]
    editor = 'false'
