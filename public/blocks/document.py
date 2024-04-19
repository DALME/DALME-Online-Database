"""Document block."""

from wagtail import blocks
from wagtail.documents.blocks import DocumentChooserBlock


class DocumentBlock(blocks.StructBlock):
    type = blocks.ChoiceBlock(
        choices=[
            ('document', 'Document'),
            ('publication', 'Publication'),
            ('talk', 'Talk'),
        ],
    )
    title = blocks.CharBlock()
    abstract = blocks.CharBlock(required=False)
    author = blocks.CharBlock()
    detail = blocks.CharBlock(required=False)
    version = blocks.FloatBlock(required=False)
    document = DocumentChooserBlock(required=False)
    url = blocks.URLBlock(required=False)
    page = blocks.PageChooserBlock(required=False)
    date = blocks.DateBlock()

    class Meta:
        icon = 'file-pdf'
        template = 'public/blocks/document.html'
