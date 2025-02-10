"""Blocks for bibliography."""

from .views import biblio_chooser_viewset

BibliographyChooserBlock = biblio_chooser_viewset.get_block_class(
    name='BibliographyChooserBlock', module_path='web.extensions.bibliography.blocks'
)
