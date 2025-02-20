"""Text Expandable block."""

from wagtail import blocks


class TextExpandableBlock(blocks.StructBlock):
    body = blocks.RichTextBlock()

    class Meta:
        icon = 'web/icons/expandable-text'
        label = 'Text (exp.)'
        template = 'extras/text_expandable_block.html'
        form_classname = 'struct-block text-expandable-block'
