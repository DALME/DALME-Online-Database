"""Enable saved search and bibliography add-ons."""

from wagtail import hooks
from wagtail.admin.rich_text.converters.html_to_contentstate import (
    ExternalLinkElementHandler,
    PageLinkElementHandler,
)

from public.handlers import (
    BibliographyElementHandler,
    BibliographyLinkHandler,
    SavedSearchElementHandler,
    SavedSearchLinkHandler,
    link_entity_decorator,
)


@hooks.register('register_rich_text_features')
def enable_savedsearch_biblio(features):
    del features.converter_rules_by_converter['contentstate']['link']
    features.register_converter_rule(
        'contentstate',
        'link',
        {
            'from_database_format': {
                'a[href]': ExternalLinkElementHandler('LINK'),
                'a[linktype="page"]': PageLinkElementHandler('LINK'),
                'a[linktype="saved_search"]': SavedSearchElementHandler('LINK'),
                'a[linktype="biblio_entry"]': BibliographyElementHandler('LINK'),
            },
            'to_database_format': {
                'entity_decorators': {'LINK': link_entity_decorator},
            },
        },
    )
    features.register_link_type(SavedSearchLinkHandler)
    features.register_link_type(BibliographyLinkHandler)
