"""Bibliography block."""

from wagtail import blocks


class BibliographyBlock(blocks.StructBlock):
    collection = blocks.ChoiceBlock(
        choices=[
            ('A4QHN348', 'Editions'),
            ('BKW2PVCM', 'Glossaries and dictionaries'),
            ('QM9AZNT3', 'Methodology'),
            ('SLIT6LID', 'Studies'),
            ('FRLVXUWL', 'Other resources'),
        ],
    )

    class Meta:
        icon = 'list-ul'
        template = 'public/blocks/_bibliography.html'
