"""URLS for the IDA's tenanted projects."""

from maintenance_mode import urls as maintenance_mode_urls
from wagtail import views

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, re_path

from api import urls as api_urls
from web.urls import urlpatterns as web_urls

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^maintenance-mode/', include(maintenance_mode_urls)),
    *web_urls,
    re_path(r'^api/', include(api_urls)),
    re_path(r'^((?:[\w\-:]+/)*)$', views.serve, name='wagtail_serve'),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]

urlpatterns += staticfiles_urlpatterns()
