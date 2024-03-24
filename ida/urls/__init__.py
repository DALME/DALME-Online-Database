"""Interface for the ida.urls module."""

from maintenance_mode import urls as maintenance_mode_urls
from wagtail import views
from wagtail.documents import urls as wagtaildocs_urls

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path

from api import urls as api_urls
from public.extensions import urlpatterns as public_extension_urls
from purl import urls as purl_urls

from .auth import urlpatterns as auth_urlpatterns
from .cms import urlpatterns as cms_urlpatterns
from .public_api import urlpatterns as public_api_urlpatterns

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^maintenance-mode/', include(maintenance_mode_urls)),
    re_path(r'^api/public/', include(public_api_urlpatterns)),
    re_path(r'^api/oauth/', include((auth_urlpatterns, 'ida'), namespace='oauth2_provider')),
    re_path(r'^api/', include(api_urls)),
    re_path(r'^purl/', include(purl_urls)),
    re_path(r'^cms/', include(cms_urlpatterns)),
    path('documents/', include(wagtaildocs_urls)),
    *public_extension_urls,
    re_path(r'^((?:[\w\-:]+/)*)$', views.serve, name='wagtail_serve'),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
]
