from django.conf.urls import include, url
from django.contrib import admin
from . import views

#postman_patterns = ([
#    url(r'^(?P<item>[a-z_-]+)/(?:(?P<option>m)/)?$', views.messaging),
#], 'postman')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^UIref/([a-z_-]+)$', views.uiref),
    url(r'^cmd/([a-z_-]+)$', views.cmd),
    url(r'^list/([a-z_-]+)$', views.list),
    url(r'^form/([a-z_-]+)$', views.form),
    url(r'^show/([a-z_-]+)/([A-Za-z0-9-]+)$', views.show),
    url(r'^tasks/', include('todo.urls')),
    #url(r'^messages/', include(postman_patterns, namespace='postman', app_name='postman')),
    #url(r'^messages/(?P<item>[a-z_-]+)/(?:(?P<option>m)/)?$', views.messaging, namespace='postman', app_name='postman'),
    url(r'^$', views.index, name='dashboard')

]
