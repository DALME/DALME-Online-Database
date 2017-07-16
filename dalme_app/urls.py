from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^UIref/([a-z_-]+)$', views.uiref),
    url(r'^$', views.index, name='dashboard')
#    url(r'^concept/(?P<concept_id>[0-9a-z-]+)/$', views.concept_detail, name='concept_detail'),
#    url(r'^dropdown_test$', views.dropdown_test, name='dropdown_test')
]
