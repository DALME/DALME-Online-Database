"""Text Expandable block."""

from wagtail import blocks


class TextExpandableBlock(blocks.StructBlock):
    body = blocks.RichTextBlock()

    class Meta:
        icon = 'expandable-text'
        template = 'text_expandable_block.html'
        form_classname = 'struct-block text-expandable-block'
