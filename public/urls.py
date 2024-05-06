"""Define cms/public URLs for the IDA."""

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.urls import include, path, reverse

from public.extensions.bibliography.urls import urlpatterns as biblio_urls
from public.extensions.footnotes.urls import urlpatterns as footnote_urls
from public.extensions.records.urls import api_router
from public.extensions.records.urls import urlpatterns as record_urls
from public.extensions.team.api import TeamAPIViewSet, UserAPIViewSet

admin.site.unregister(Group)


def to_ida_login(_request):
    """Redirect request to login page."""
    return auth_views.redirect_to_login(reverse('wagtailadmin_home'), login_url=settings.LOGIN_URL)


def to_ida_logout(_request):
    """Redirect request to logout page."""
    return redirect(settings.LOGOUT_URL)


api_router.register_endpoint('team', TeamAPIViewSet)
api_router.register_endpoint('user', UserAPIViewSet)

cmsurls = [
    *biblio_urls,
    *footnote_urls,
    *record_urls,
    path('', include(wagtailadmin_urls)),
]

urlpatterns = [
    path('api/public/', api_router.urls, name='public_api_endpoints'),
    path('cms/login/', to_ida_login, name='wagtailadmin_login'),
    path('cms/logout/', to_ida_logout, name='wagtailadmin_logout'),
    path('cms/', include(cmsurls)),
    path('documents/', include(wagtaildocs_urls)),
]
