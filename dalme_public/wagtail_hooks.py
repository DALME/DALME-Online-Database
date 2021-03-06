from dalme_public.handlers import SavedSearchLinkHandler, link_entity_search, SavedSearchElementHandler
from django.utils.html import format_html
from django.urls import reverse
from wagtail.admin.rich_text.converters.html_to_contentstate import PageLinkElementHandler, ExternalLinkElementHandler
from wagtail.core import hooks


@hooks.register('insert_editor_js')
def editor_js():
    return format_html(
        """
        <script>
            window.chooserUrls['pageChooser'] = '{}';
            window.chooserUrls['savedSearchChooser'] = '{}';
        </script>
        """,
        reverse('wagtailadmin_chooser_page_reroute'),
        reverse('wagtailadmin_choose_page_saved_search')
    ) + """
        <script>
            $(document).ready(function () {
                PAGE_CHOOSER_MODAL_ONLOAD_HANDLERS['saved_search'] = function(modal, jsonData) {
                    $('p.link-types a', modal.body).on('click', function() {
                        modal.loadUrl(this.href);
                        return false;
                    });

                    $('form', modal.body).on('submit', function() {
                        modal.postForm(this.action, $(this).serialize());
                        return false;
                    });
                };
                PAGE_CHOOSER_MODAL_ONLOAD_HANDLERS['saved_search_chosen'] = function(modal, jsonData) {
                    modal.respond('pageChosen', jsonData['result']);
                    modal.close();
                };
            });
        </script>
        """


@hooks.register('register_rich_text_features')
def register_saved_search(features):
    del features.converter_rules_by_converter['contentstate']['link']
    features.register_converter_rule('contentstate', 'link', {
        'from_database_format': {
            'a[href]': ExternalLinkElementHandler('LINK'),
            'a[linktype="page"]': PageLinkElementHandler('LINK'),
            'a[linktype="saved_search"]': SavedSearchElementHandler('LINK'),
        },
        'to_database_format': {
            'entity_decorators': {'LINK': link_entity_search}
        }
    })
    features.register_link_type(SavedSearchLinkHandler)
