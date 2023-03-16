"""Define URLs for dalme_purl."""
from rest_framework import routers

from django.urls import include, path

from dalme_purl import api

router = routers.DefaultRouter()
router.register(r'', api.Endpoint, basename='endpoint')

urlpatterns = [
    path('', include((router.urls, 'dalme_purl'), namespace='purl')),
]
