"""Hooks for bibliography extension."""

import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail import hooks

from django.urls import reverse
from django.utils.html import format_html

from .rich_text import ReferenceLinkHandler
from .rich_text.contentstate import ReferenceElementHandler, reference_decorator
from .views import BiblioChooserViewSet, BiblioViewSet

hooks.register('register_admin_viewset', BiblioViewSet)
hooks.register('register_admin_viewset', BiblioChooserViewSet)


@hooks.register('insert_editor_js')
def add_reference_js_to_editor():
    return format_html(
        """
            <script type="text/javascript">
                window.chooserUrls.referenceChooser = '{}';
            </script>
        """,
        reverse('reference_chooser'),
    )


@hooks.register('register_rich_text_features')
def register_reference_feature(features):
    features.default_features.append('reference')
    feature_name = 'reference'
    type_ = 'REFERENCE'

    control = {
        'type': type_,
        'icon': 'book',
        'description': 'Bibliographic reference',
    }

    features.register_editor_plugin(
        'draftail',
        feature_name,
        draftail_features.EntityFeature(
            control,
            js=[
                'js/reference-chooser-select.js',
                'js/reference-chooser-modal.js',
            ],
            css={'all': ['css/reference-chooser.css']},
        ),
    )

    features.register_converter_rule(
        'contentstate',
        feature_name,
        {
            'from_database_format': {'a[data-reference]': ReferenceElementHandler(type_)},
            'to_database_format': {'entity_decorators': {type_: reference_decorator}},
        },
    )

    features.register_link_type(ReferenceLinkHandler)


@hooks.register('register_icons')
def register_extra_icons(icons):
    return [
        *icons,
        'wagtailfontawesomesvg/solid/book.svg',
    ]
