"""Hooks for footnotes extension."""

import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail import hooks

from django.urls import reverse
from django.utils.html import format_html

from .rich_text import FootnoteLinkHandler
from .rich_text.contentstate import FootnoteElementHandler, footnote_decorator


@hooks.register('insert_editor_js')
def add_footnotes_js_to_editor():
    return format_html(
        """
            <script type="text/javascript">
                window.chooserUrls.footnoteEntry = '{}';
            </script>
        """,
        reverse('footnote_chooser'),
    )


@hooks.register('register_rich_text_features')
def enable_footnotes(features):
    features.default_features.append('footnote')
    feature_name = 'footnote'
    type_ = 'FOOTNOTE'

    control = {
        'type': type_,
        'icon': 'asterisk',
        'description': 'Footnote',
    }

    features.register_editor_plugin(
        'draftail',
        feature_name,
        draftail_features.EntityFeature(
            control,
            js=['js/footnote-chooser-modal.js'],
            css={
                'all': [
                    'css/footnote-decorator.css',
                    'css/footnote-chooser.css',
                ]
            },
        ),
    )

    features.register_converter_rule(
        'contentstate',
        feature_name,
        {
            'from_database_format': {'a[data-footnote]': FootnoteElementHandler(type_)},
            'to_database_format': {'entity_decorators': {type_: footnote_decorator}},
        },
    )

    features.register_link_type(FootnoteLinkHandler)


@hooks.register('before_serve_page')
def add_footnotes(page, _request, _serve_args, _serve_kwargs):
    if page.has_footnotes:
        page.footnote_list = page.footnotes.all()
    return page
