from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from ._common import DALMEListView


@method_decorator(login_required, name='dispatch')
class PlaceList(DALMEListView):
    page_title = 'Places'
    dt_config = 'places'
    breadcrumb = [('Entities', ''), ('Places', '/places')]
