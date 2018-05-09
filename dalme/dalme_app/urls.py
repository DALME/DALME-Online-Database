from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^UIref/([a-z_-]+)$', views.uiref),
    url(r'^script/([a-z_-]+)$', views.script),
    url(r'^list/(?P<module>[a-z_-]+)(?:/(?P<type>[a-zA-Z]+))?/$', views.list),
    url(r'^form/([a-z_-]+)$', views.form),
    url(r'^show/([a-z_-]+)/([A-Za-z0-9-]+)$', views.show),
    url(r'^$', views.index, name='dashboard'),
]
