"""Model footnote data."""

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.fields import RichTextField
from wagtail.models import Page

from django.db.models import UUIDField


class Footnote(ClusterableModel):
    id = UUIDField(primary_key=True)
    page = ParentalKey(Page, related_name='footnotes')
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
