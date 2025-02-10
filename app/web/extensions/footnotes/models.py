"""Model footnote data."""

import re

from modelcluster.fields import ParentalKey
from wagtail.fields import RichTextField
from wagtail.models import Orderable, Page

from django.db import models

FOOTNOTE_ID = re.compile(r'data-footnote="(\w{8}-\w{4}-\w{4}-\w{4}-\w{12})"', re.IGNORECASE)


class Footnote(Orderable):
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


class FootnoteMixin(models.Model):
    has_footnotes = models.BooleanField(default=False, null=True, blank=True)
    has_placemarker = models.BooleanField(default=False, null=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """Override the save method to populate state fields and add footnotes as relations."""
        raw_content = str(self.body.raw_data)
        self.has_footnotes = 'data-footnote=' in raw_content
        self.has_placemarker = 'footnotes_placemarker' in raw_content
        if self.has_footnotes:
            footnote_ids = FOOTNOTE_ID.findall(raw_content)

            if not self._state.adding:  # existing page
                this_page_fns = list(Footnote.objects.filter(page_id=self.id))  # all footnotes saved for this page
                for fn in this_page_fns:
                    if str(fn) not in footnote_ids:  # fn removed from page, we delete it
                        fn.delete()

            ordered = sorted(Footnote.objects.filter(id__in=footnote_ids), key=lambda x: footnote_ids.index(str(x)))
            footnotes = []
            for idx, fn in enumerate(ordered, start=1):
                fn.sort_order = idx
                footnotes.append(fn)
            self.footnotes = footnotes

        return super().save(*args, **kwargs)
