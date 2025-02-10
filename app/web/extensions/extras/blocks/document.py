"""Document block."""

from wagtail import blocks
from wagtail.documents.blocks import DocumentChooserBlock

from web.extensions.extras.widgets import CustomSelect


class DocumentBlock(blocks.StructBlock):
    type = blocks.ChoiceBlock(
        choices=[
            ('document', 'Document'),
            ('publication', 'Publication'),
            ('talk', 'Talk'),
        ],
        help_text='Type of document.',
        widget=CustomSelect,
    )
    version = blocks.DecimalBlock(required=False, help_text='Version, if applicable.')
    date = blocks.DateBlock(help_text='Date (e.g. creation, publication, etc.')
    title = blocks.CharBlock(help_text='Title for this entry.')
    author = blocks.CharBlock(help_text='Name of the author(s) for this entry.')
    detail = blocks.CharBlock(
        required=False,
        help_text='Additional information, e.g. press/place of publication, location of the talk, etc.',
    )
    abstract = blocks.RichTextBlock(
        editor='minimal',
        required=False,
        help_text='Abstract for this entry, if applicable.',
    )
    url = blocks.URLBlock(required=False, help_text='Related URL, e.g. link to online resource, press site, etc.')
    document = DocumentChooserBlock(required=False, help_text='Document file (e.g. PDF).')
    page = blocks.PageChooserBlock(required=False, help_text='Add a link to a page on this site.')

    class Meta:
        icon = 'file-pdf'
        template = 'document_block.html'
        form_classname = 'struct-block document-block'
        form_template = 'document_form.html'
