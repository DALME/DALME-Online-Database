"""Define top-level application URLs."""
from maintenance_mode import urls as maintenance_mode_urls
from wagtail import views
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from django.urls import include, path, re_path, reverse

from dalme_api import urls as api_urls
from dalme_public import api
from dalme_public.views import (
    biblio_entry,
    enter_footnote,
    reroute_chooser,
    saved_search,
)
from dalme_purl import urls as purl_urls


def to_dalme_login(_request):
    """Redirect request to login page."""
    return auth_views.redirect_to_login(reverse('wagtailadmin_home'), login_url=settings.LOGIN_URL)


def to_dalme_logout(_request):
    """Redirect request to logout page."""
    return redirect(settings.LOGOUT_URL)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('maintenance-mode/', include(maintenance_mode_urls)),
    path('api/public/records/', api.RecordList.as_view(), name='record_list'),
    path('api/public/records/<uuid:pk>/', api.RecordDetail.as_view(), name='record_detail'),
    path('api/public/choices/', api.FilterChoices.as_view(), name='filter_choices'),
    path('api/public/thumbnails/', api.Thumbnail.as_view(), name='thumbnails'),
    path('api/', include(api_urls)),
    path('purl/', include(purl_urls)),
    # path('core/', include(core_urls)),
    path('cms/login/', to_dalme_login, name='wagtailadmin_login'),
    path('cms/logout/', to_dalme_logout, name='wagtailadmin_logout'),
    path('cms/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    path('choose-saved-search/', saved_search, name='wagtailadmin_choose_page_saved_search'),
    path('choose-bibliography/', biblio_entry, name='wagtailadmin_choose_bibliography'),
    path('enter-footnote/', enter_footnote, name='wagtailadmin_enter_footnote'),
    path('choose-reroute/', reroute_chooser, name='wagtailadmin_chooser_page_reroute'),
    path('choose-reroute/<slug:route>/', reroute_chooser, name='wagtailadmin_chooser_page_reroute_child'),
    re_path(r'^((?:[\w\-:]+/)*)$', views.serve, name='wagtail_serve'),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]
