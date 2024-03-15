"""Model base image data."""

from wagtail.images.models import AbstractImage, AbstractRendition, Image

from django.db import models


class BaseImage(AbstractImage):
    caption = models.CharField(max_length=255, null=True, blank=True)
    admin_form_fields = (*Image.admin_form_fields, 'caption')


class CustomRendition(AbstractRendition):
    image = models.ForeignKey(BaseImage, on_delete=models.CASCADE, related_name='renditions')

    class Meta:
        unique_together = ('image', 'filter_spec', 'focal_point_key')
