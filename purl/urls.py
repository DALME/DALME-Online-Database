"""Define URLs for purl."""

from rest_framework import routers

from django.urls import include, path

from purl import api

router = routers.DefaultRouter()
router.register(r'', api.Endpoint, basename='endpoint')

urlpatterns = [
    path('', include((router.urls, 'purl'), namespace='purl')),
]
