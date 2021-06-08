from dalme_public.handlers import SavedSearchLinkHandler, link_entity_search, SavedSearchElementHandler
from django.utils.html import format_html
from django.urls import reverse
from wagtail.admin.rich_text.converters.html_to_contentstate import PageLinkElementHandler, ExternalLinkElementHandler
from wagtail.core import hooks
from django.templatetags.static import static
from django.shortcuts import redirect


@hooks.register('construct_settings_menu')
def hide_users_menu_item(request, menu_items):
    menu_items[:] = [item for item in menu_items if item.name not in ['users', 'groups']]


@hooks.register('insert_global_admin_css', order=0)
def extra_admin_css():
    return format_html('<link rel="stylesheet" href="{}">', static("css/dalme_public/dalme_public_admin.css"))


@hooks.register('before_serve_page')
def redirects(page, request, serve_args, serve_kwargs):
    if page.is_root():
        home = page.get_children().live().first()
        return redirect(home.url, permanent=False)
    if page._meta.label == 'dalme_public.Section':
        url = page.get_children().live().first().url
        return redirect(url, permanent=False)


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
