"""Hooks for records extension."""

import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail import hooks

from django.urls import reverse
from django.utils.html import format_html

from .rich_text import SavedSearchLinkHandler
from .rich_text.contentstate import SavedSearchElementHandler, saved_search_decorator


@hooks.register('insert_editor_js')
def add_saved_search_js_to_editor():
    return format_html(
        """
            <script type="text/javascript">
                window.chooserUrls.savedSearchChooser = '{}';
            </script>
        """,
        reverse('saved_search_chooser'),
    )


@hooks.register('register_rich_text_features')
def register_saved_search_feature(features):
    features.default_features.append('saved_search')
    feature_name = 'saved_search'
    type_ = 'SAVED_SEARCH'

    control = {
        'type': type_,
        'icon': 'magnifying-glass-location',
        'description': 'Saved search',
    }

    features.register_editor_plugin(
        'draftail',
        feature_name,
        draftail_features.EntityFeature(
            control,
            js=['js/saved-search-chooser-modal.js'],
            css={'all': ['css/saved-search-chooser.css']},
        ),
    )

    features.register_converter_rule(
        'contentstate',
        feature_name,
        {
            'from_database_format': {'a[data-saved-search]': SavedSearchElementHandler(type_)},
            'to_database_format': {'entity_decorators': {type_: saved_search_decorator}},
        },
    )

    features.register_link_type(SavedSearchLinkHandler)
