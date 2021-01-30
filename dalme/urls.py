"""dalme URL Configuration"""
# from django.urls import path, re_path, include
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from wagtail.admin import urls as wagtailadmin_urls
# from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

urlpatterns = [
    # re_path(r'^', include('dalme_app.urls')),
    # Public URLs. Wagtail didn't like being namespaced so leave at top-level for now.
    path('cms/', include(wagtailadmin_urls)),
    # path('public/', include(wagtail_urls)),
    path('documents/', include(wagtaildocs_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
