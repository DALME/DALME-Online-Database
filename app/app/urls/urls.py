"""URLS for the app."""

from maintenance_mode import urls as maintenance_mode_urls

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, re_path
from django.views.generic import TemplateView

from domain.api.router import router
from oauth.urls import urls as auth_urls

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^maintenance-mode/', include(maintenance_mode_urls)),
    re_path(r'^api/oauth/', include((auth_urls, 'oauth'), namespace='oauth2_provider')),
    re_path(r'^api/api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    re_path(r'^api/', include((router.urls, 'api'), namespace='api')),
    re_path(r'^$', TemplateView.as_view(template_name='web/home.html')),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]

urlpatterns += staticfiles_urlpatterns()
