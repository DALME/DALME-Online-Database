"""Models for images extension."""

from wagtail.images.models import (
    AbstractImage,
    AbstractRendition,
    Image,
    WagtailImageField,
    get_rendition_storage,
    get_rendition_upload_to,
    get_upload_to,
)

from django.db import models


class BaseImage(AbstractImage):
    caption = models.CharField(max_length=255, null=True, blank=True)
    admin_form_fields = (*Image.admin_form_fields, 'caption')
    # we need to override the image field because by default it is limited
    # to 100 characters and certain existing images go over when we add the
    # tenant prefix in data migrations
    file = WagtailImageField(
        verbose_name='file',
        upload_to=get_upload_to,
        width_field='width',
        height_field='height',
        max_length=255,
    )


class CustomRendition(AbstractRendition):
    image = models.ForeignKey(BaseImage, on_delete=models.CASCADE, related_name='renditions')
    file = WagtailImageField(
        upload_to=get_rendition_upload_to,
        storage=get_rendition_storage,
        width_field='width',
        height_field='height',
        max_length=255,
    )

    class Meta:
        unique_together = ('image', 'filter_spec', 'focal_point_key')
