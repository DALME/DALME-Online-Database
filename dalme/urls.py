"""dalme URL Configuration
"""
from django.urls import path, re_path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.http import HttpResponse
from allaccess.views import OAuthRedirect
from rest_framework import routers
from dalme_app import views, apis

router = routers.DefaultRouter()
router.register(r'sources', apis.Sources, basename='sources')
router.register(r'users', apis.Users, basename='users')
router.register(r'models', apis.Models, basename='models')
router.register(r'transcriptions', apis.Transcriptions, basename='transcriptions')
router.register(r'images', apis.Images, basename='images')
router.register(r'pages', apis.Pages, basename='pages')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('accounts/login/<slug:provider>/', OAuthRedirect.as_view(), name='allaccess-login'),
    path('accounts/callback/<slug:provider>/', views.OAuthCallback_WP.as_view(provider_id = 'ID'), name='allaccess-callback'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('django_admin/doc/', include('django.contrib.admindocs.urls')),
    path('django_admin/', admin.site.urls),
    re_path(r'^\.well-known/acme-challenge/DWY9GSDZjOsijpklS3RIAuBvZt2PThO7ameePcaIHm8/', lambda request: HttpResponse('DWY9GSDZjOsijpklS3RIAuBvZt2PThO7ameePcaIHm8.LbUmj5n5DqTPM7bapjsa-DennAErlpafYkGP-9eZzzo'), name='hello_world'),
    re_path(r'^', include('dalme_app.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
