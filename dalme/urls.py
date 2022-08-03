from django.urls import path, include, re_path, reverse
from dalme_public import api
from django.conf import settings
from django.conf.urls.static import static
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from dalme_api import urls as api_urls
from dalme_purl import urls as purl_urls
from dalme_app import urls as core_urls
from django.contrib.auth import views as auth_views
from wagtail import views
from dalme_public.views import enter_footnote, saved_search, reroute_chooser, biblio_entry


def to_dalme_login(request):
    return auth_views.redirect_to_login(reverse('wagtailadmin_home'), login_url=settings.LOGIN_URL)


urlpatterns = [
    path('api/public/sources/', api.SourceList.as_view(), name='source_list'),
    path('api/public/sources/<uuid:pk>/', api.SourceDetail.as_view(), name='source_detail'),
    path('api/public/choices/', api.FilterChoices.as_view(), name='filter_choices'),
    path('api/public/thumbnails/', api.Thumbnail.as_view(), name='thumbnails'),
    path('api/', include(api_urls)),
    path('purl/', include(purl_urls)),
    path('core/', include(core_urls)),
    path('cms/login/', to_dalme_login, name='wagtailadmin_login'),
    path('cms/logout/', auth_views.LogoutView.as_view(), name='wagtailadmin_logout'),
    path('cms/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    path('choose-saved-search/', saved_search, name='wagtailadmin_choose_page_saved_search'),
    path('choose-bibliography/', biblio_entry, name='wagtailadmin_choose_bibliography'),
    path('enter-footnote/', enter_footnote, name='wagtailadmin_enter_footnote'),
    path('choose-reroute/', reroute_chooser, name='wagtailadmin_chooser_page_reroute'),
    path('choose-reroute/<slug:route>/', reroute_chooser, name='wagtailadmin_chooser_page_reroute_child'),
    re_path(r'^((?:[\w\-:]+/)*)$', views.serve, name='wagtail_serve')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns = [
#         path('__debug__/', include(debug_toolbar.urls)),
#     ] + urlpatterns
