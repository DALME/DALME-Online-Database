"""Define cms/public URLs for the IDA."""

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.documents import urls as wagtaildocs_urls

from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.urls import include, path, reverse

from public.api import FilterChoices, RecordsAPIViewSet, Thumbnail
from public.extensions.bibliography.urls import urlpatterns as biblio_urls
from public.extensions.footnotes.api import FootnotesAPIViewSet
from public.extensions.footnotes.urls import urlpatterns as footnote_urls
from public.extensions.records.urls import urlpatterns as record_urls

api_router = WagtailAPIRouter('wagtailapi')

api_router.register_endpoint('footnotes', FootnotesAPIViewSet)
api_router.register_endpoint('records', RecordsAPIViewSet)
api_router.register_endpoint('choices', FilterChoices)
api_router.register_endpoint('thumbnails', Thumbnail)

admin.site.unregister(Group)


def to_ida_login(_request):
    """Redirect request to login page."""
    return auth_views.redirect_to_login(reverse('wagtailadmin_home'), login_url=settings.LOGIN_URL)


def to_ida_logout(_request):
    """Redirect request to logout page."""
    return redirect(settings.LOGOUT_URL)


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
