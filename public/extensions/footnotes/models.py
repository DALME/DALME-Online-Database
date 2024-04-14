"""Model footnote data."""

import re

from modelcluster.fields import ParentalKey
from wagtail.fields import RichTextField
from wagtail.models import Page

from django.db import models

FOOTNOTE_ID = re.compile(r'data-footnote="(\w{8}-\w{4}-\w{4}-\w{4}-\w{12})"', re.IGNORECASE)


class Footnote(models.Model):
    id = models.UUIDField(primary_key=True)
    page = ParentalKey(Page, related_name='footnotes', null=True, blank=True, on_delete=models.CASCADE)
    text = RichTextField(
        features=[
            'bold',
            'italic',
            'ol',
            'ul',
            'link',
            'document-link',
            'code',
            'superscript',
            'subscript',
            'strikethrough',
            'blockquote',
            'reference',
        ]
    )

    class Meta:
        unique_together = ('page', 'id')

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        """Override the save method to deal with new pages which try to create related entities instead of updating."""
        if self.page and self.text == '':  # new page creation
            self._state.adding = False
            return super().save(update_fields=['page'], force_update=True)

        if kwargs.pop('edit_mode'):
            self._state.adding = False

        return super().save(*args, **kwargs)


class FootnoteMixin(models.Model):
    has_footnotes = models.BooleanField(default=False, null=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """Override the save method to populate has_footnotes field and add footnotes as relation."""
        if 'data-footnote=' in str(self.body.raw_data):
            self.has_footnotes = True
            if self._state.adding:
                footnote_ids = FOOTNOTE_ID.findall(str(self.body.raw_data))
                self.footnotes = [Footnote(id=fn_id) for fn_id in footnote_ids]
        return super().save(*args, **kwargs)
