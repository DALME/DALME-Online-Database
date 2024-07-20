"""URLS for the IDA public site."""

from maintenance_mode import urls as maintenance_mode_urls
from oauth2_provider import urls
from oauth2_provider import views as oauth2_views

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, re_path
from django.views.generic import TemplateView

from api import urls as api_urls
from ida import auth
from purl import urls as purl_urls

auth_urls = [
    re_path(r'^authorize/$', oauth2_views.AuthorizationView.as_view(), name='authorize'),
    re_path(r'^authorize/callback/$', auth.AuthorizationCode.as_view(), name='authorization-code'),
    re_path(r'^login/$', auth.Login.as_view(), name='login'),
    re_path(r'^token/$', auth.OAuthToken.as_view(), name='token'),
    re_path(r'^revoke-token/$', oauth2_views.RevokeTokenView.as_view(), name='revoke-token'),
    re_path(r'^introspect/$', oauth2_views.IntrospectTokenView.as_view(), name='introspect'),
    *urls.management_urlpatterns + urls.oidc_urlpatterns,
]

urlpatterns = [
    re_path(r'', TemplateView.as_view(template_name='home.html')),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^maintenance-mode/', include(maintenance_mode_urls)),
    re_path(r'^api/oauth/', include((auth_urls, 'ida'), namespace='oauth2_provider')),
    re_path(r'^api/', include(api_urls)),
    re_path(r'^purl/', include(purl_urls)),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]

urlpatterns += staticfiles_urlpatterns()
