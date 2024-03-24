"""Hooks for bibliography extension."""

import wagtail.admin.rich_text.editors.draftail.features as draftail_features

from django.urls import reverse
from django.utils.html import format_html

from .handlers import ReferenceElementHandler, reference_entity_decorator

# def add_biblio_js_to_editor():
#     return (
#         format_html(
#             """
#             <script type="text/javascript">
#                 window.chooserUrls['referenceChooser'] = '{}';
#             </script>
#             """,
#             reverse('wagtailadmin_choose_reference'),
#         )
#         + """
#             <script type="text/javascript">
#                 $(document).ready(function () {
#                     PAGE_CHOOSER_MODAL_ONLOAD_HANDLERS['reference'] = function(modal, jsonData) {
#                         $('p.link-types a', modal.body).on('click', function() {
#                             modal.loadUrl(this.href);
#                             return false;
#                         });

#                         $('form', modal.body).on('submit', function() {
#                             modal.postForm(this.action, $(this).serialize());
#                             return false;
#                         });
#                     };
#                     PAGE_CHOOSER_MODAL_ONLOAD_HANDLERS['reference_chosen'] = function(modal, jsonData) {
#                         modal.respond('pageChosen', jsonData['result']);
#                         modal.close();
#                     };
#                 });
#             </script>
#         """
#     )


def add_reference_js_to_editor():
    return format_html(
        """
        <script>
            window.chooserUrls.referenceChooser = '{}';
        </script>
        """,
        reverse('reference_chooser:choose'),
    )


def register_reference_feature(features):
    features.default_features.append('reference')
    feature_name = 'reference'
    type_ = 'REFERENCE'

    control = {
        'type': type_,
        'label': '$',
        'description': 'Reference',
    }

    features.register_editor_plugin(
        'draftail',
        feature_name,
        draftail_features.EntityFeature(
            control,
            js=['js/extensions/reference-chooser-modal.js'],
        ),
    )

    features.register_converter_rule(
        'contentstate',
        feature_name,
        {
            'from_database_format': {'span[data-stock]': ReferenceElementHandler(type_)},
            'to_database_format': {'entity_decorators': {type_: reference_entity_decorator}},
        },
    )
