from django.urls import path, include
from rest_framework import routers
from dalme_purl import api

router = routers.DefaultRouter()
router.register(r'', api.Endpoint, basename='endpoint')

urlpatterns = [
    path('', include((router.urls, 'dalme_purl'), namespace='purl')),
]
