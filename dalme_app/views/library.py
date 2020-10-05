from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from ._common import DALMEListView


@method_decorator(login_required, name='dispatch')
class LibraryList(DALMEListView):
    page_title = 'Library'
    dt_config = 'library'
    breadcrumb = [('Project', ''), ('Library', '/library')]
    editor = 'false'
    helpers = ['zotero_rendering']
