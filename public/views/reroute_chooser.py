"""View for rerouting chooser modals."""

import urllib

from django.http import HttpResponseRedirect
from django.urls import reverse


def reroute_chooser(request, route=None):
    params = urllib.parse.urlencode(request.GET)

    if route:
        if str(route).isdigit():
            rev = reverse('wagtailadmin_choose_page_child', args=[route])
        elif route == 'saved_search':
            rev = reverse('wagtailadmin_choose_page_saved_search')
        elif route == 'biblio_entry':
            rev = reverse('wagtailadmin_choose_bibliography')
    else:
        rev = reverse('wagtailadmin_choose_page')

    if params:
        rev = f'{rev}?{params}'

    return HttpResponseRedirect(rev)
