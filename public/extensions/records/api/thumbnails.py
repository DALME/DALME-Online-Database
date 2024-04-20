"""API endpoints for records extension."""

from django.http import JsonResponse
from django.urls import path
from django.views import View

from ida.models.resourcespace import rs_resource


class ThumbnailsAPI(View):
    """API endpoint for returning thumbnails."""

    @classmethod
    def get_urlpatterns(cls):
        return [path('', cls.as_view(), name='thumbnails')]

    def get_data(self):
        """Get the thumbnail's URL."""
        try:
            thumbnail = rs_resource.objects.get(
                ref=self.request.GET['image_ref'],
            ).get_image_url(self.request.GET['size'])
        except (KeyError, ValueError):
            thumbnail = None
        return {'image_url': thumbnail}

    def get(self, request):  # noqa: ARG002
        """Return thumbnail URL."""
        return JsonResponse(self.get_data())
