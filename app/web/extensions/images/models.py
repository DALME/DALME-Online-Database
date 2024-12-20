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

from app.context import get_current_tenant


class BaseImage(AbstractImage):
    caption = models.CharField(max_length=255, null=True, blank=True)
    admin_form_fields = (*Image.admin_form_fields, 'caption')
    file = WagtailImageField(
        verbose_name='file',
        upload_to=get_upload_to,
        width_field='width',
        height_field='height',
        max_length=255,
    )

    def get_upload_to(self, filename):
        """We override this method to add the current tenant to the path."""
        full_path = super().get_upload_to(filename)
        return f'{get_current_tenant()}/{full_path}'


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

    def get_upload_to(self, filename):
        """We override this method to add the current tenant to the path."""
        full_path = super().get_upload_to(filename)
        return f'{get_current_tenant()}/{full_path}'
