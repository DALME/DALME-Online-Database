"""Define a code block."""

from wagtail.blocks import ChoiceBlock, TextBlock
from wagtailcodeblock.blocks import CodeBlock as BaseCodeBlock

from web.extensions.extras.widgets import CustomSelect


class CodeBlock(BaseCodeBlock):
    """Subclass of CodeBlock from wagtailcodeblock to work around bug with language choice."""

    # see: https://github.com/wagtail/wagtail/pull/11958
    def __init__(self, local_blocks=None, **kwargs):
        self.INCLUDED_LANGUAGES = (
            ('html', 'HTML'),
            ('mathml', 'MathML'),
            ('svg', 'SVG'),
            ('xml', 'XML'),
        )

        local_blocks = [] if local_blocks is None else local_blocks.copy()
        language_choices, language_default = self.get_language_choice_list(**kwargs)

        local_blocks.extend(
            [
                (
                    'language',
                    ChoiceBlock(
                        choices=language_choices,
                        label='Language',
                        default=language_default,
                        identifier='language',
                        widget=CustomSelect,
                    ),
                ),
                ('code', TextBlock(label='Code', identifier='code')),
            ]
        )

        super(BaseCodeBlock, self).__init__(local_blocks, **kwargs)
