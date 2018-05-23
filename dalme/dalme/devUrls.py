"""dalme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.http import HttpResponse
from dalme_app import views


urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'login.html', 'redirect_authenticated_user': True}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'https://dalme.org'}, name='logout'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^\.well-known/acme-challenge/DWY9GSDZjOsijpklS3RIAuBvZt2PThO7ameePcaIHm8/', lambda request: HttpResponse('DWY9GSDZjOsijpklS3RIAuBvZt2PThO7ameePcaIHm8.LbUmj5n5DqTPM7bapjsa-DennAErlpafYkGP-9eZzzo'), name='hello_world'),
    url(r'^', include('dalme_app.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
