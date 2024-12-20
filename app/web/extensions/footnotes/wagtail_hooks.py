"""Hooks for footnotes extension."""

import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail import hooks

from django.urls import reverse_lazy

from .rich_text import FootnoteLinkHandler
from .rich_text.contentstate import FootnoteElementHandler, footnote_decorator


@hooks.register('register_rich_text_features')
def enable_footnotes(features):
    features.default_features.append('footnote')
    feature_name = 'footnote'
    type_ = 'FOOTNOTE'

    control = {
        'type': type_,
        'icon': 'asterisk',
        'description': 'Footnote',
        'chooserUrls': {'footnoteEntry': reverse_lazy('footnote_chooser')},
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
    if getattr(page, 'has_footnotes', False):
        page.footnote_list = page.footnotes.all()
    return page


@hooks.register('register_icons')
def register_extra_icons(icons):
    return [
        *icons,
        'wagtailfontawesomesvg/solid/asterisk.svg',
    ]
