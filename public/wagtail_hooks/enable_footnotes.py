"""Enable footnotes."""

import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail import hooks

from public.handlers import FootnoteElementHandler, footnote_decorator


@hooks.register('register_rich_text_features')
def enable_footnotes(features):
    features.default_features.append('footnote')
    feature_name = 'footnote'
    type_ = 'FOOTNOTE'

    control = {
        'type': type_,
        'icon': [
            'M917.5,83.3c0-10.7-10.3-19.4-23-19.4H123.7c-12.7,0-23,8.7-23,19.4v854.4c0,10.7,10.3,19.4,23,19.4h770.8c12.7,0,23-8.7,23-19.4L917.5,83.3L917.5,83.3z',
            'M962.1,84.4c0-32.2-30.8-58.3-68.9-58.3H125.1c-38.1,0-68.9,26.1-68.9,58.3v854.5c0,32.2,30.9,58.3,68.9,58.3h768.1c38.1,0,68.9-26.1,68.9-58.3L962.1,84.4L962.1,84.4z M884.1,907.3c0,9.9-9.5,17.9-21.2,17.9H151.1c-11.7,0-21.2-8-21.2-17.9v-789c0-9.9,9.5-17.9,21.2-17.9h711.8c11.7,0,21.2,8,21.2,17.9L884.1,907.3L884.1,907.3z',
            'M429.9,420.5h360.4v70H429.9V420.5z M223.7,530.3h566.6v70H223.7V530.3z M223.7,642.5h566.6v70H223.7V642.5z M223.7,753.3h566.6v70H223.7V753.3z M268.4,182.4h117.3v306.8H268.4V182.4z M225.8,285.1h42.5v-64.8h-42.5V285.1z',
        ],
        'description': 'Insert footnote',
    }

    features.register_editor_plugin(
        'draftail',
        feature_name,
        draftail_features.EntityFeature(
            control,
            js=['js/public_footnote.js'],
            css={'all': ['css/public_footnote.css']},
        ),
    )

    features.register_converter_rule(
        'contentstate',
        feature_name,
        {
            'from_database_format': {'span[data-footnote]': FootnoteElementHandler(type_)},
            'to_database_format': {'entity_decorators': {type_: footnote_decorator}},
        },
    )
