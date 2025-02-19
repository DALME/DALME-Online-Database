"""Hooks for records extension."""

import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail import hooks

from django.urls import reverse_lazy

from .rich_text import SavedSearchLinkHandler
from .rich_text.contentstate import SavedSearchElementHandler, saved_search_decorator
from .views import CollectionChooserViewSet, RecordChooserViewSet

hooks.register('register_admin_viewset', RecordChooserViewSet)
hooks.register('register_admin_viewset', CollectionChooserViewSet)


@hooks.register('register_rich_text_features')
def register_saved_search_feature(features):
    features.default_features.append('saved_search')
    feature_name = 'saved_search'
    type_ = 'SAVED_SEARCH'

    control = {
        'type': type_,
        'icon': 'magnifying-glass-location',
        'description': 'Saved search',
        'chooserUrls': {'savedSearchChooser': reverse_lazy('saved_search_chooser')},
    }

    features.register_editor_plugin(
        'draftail',
        feature_name,
        draftail_features.EntityFeature(
            control,
            js=['web/extensions/records/js/saved-search-chooser-modal.js'],
            css={'all': ['web/extensions/records/css/saved-search-chooser.css']},
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


@hooks.register('register_icons')
def register_extra_icons(icons):
    return [
        *icons,
        'wagtailfontawesomesvg/solid/layer-group.svg',
        'wagtailfontawesomesvg/solid/file-lines.svg',
        'wagtailfontawesomesvg/solid/magnifying-glass-location.svg',
        'wagtailfontawesomesvg/solid/folder-plus.svg',
    ]
