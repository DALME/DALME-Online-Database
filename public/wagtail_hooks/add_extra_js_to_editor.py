"""Add additional javascript to editor."""

from wagtail import hooks

from django.urls import reverse
from django.utils.html import format_html


@hooks.register('insert_editor_js')
def add_extra_js_to_editor():
    return (
        format_html(
            """
        <script>
            window.chooserUrls['pageChooser'] = '{}';
            window.chooserUrls['savedSearchChooser'] = '{}';
            window.chooserUrls['bibliographyChooser'] = '{}';
            window.chooserUrls['footnoteEntry'] = '{}';
        </script>
        """,
            reverse('wagtailadmin_chooser_page_reroute'),
            reverse('wagtailadmin_choose_page_saved_search'),
            reverse('wagtailadmin_choose_bibliography'),
            reverse('wagtailadmin_enter_footnote'),
        )
        + """
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
                PAGE_CHOOSER_MODAL_ONLOAD_HANDLERS['biblio_entry'] = function(modal, jsonData) {
                    $('p.link-types a', modal.body).on('click', function() {
                        modal.loadUrl(this.href);
                        return false;
                    });

                    $('form', modal.body).on('submit', function() {
                        modal.postForm(this.action, $(this).serialize());
                        return false;
                    });
                };
                PAGE_CHOOSER_MODAL_ONLOAD_HANDLERS['biblio_chosen'] = function(modal, jsonData) {
                    modal.respond('pageChosen', jsonData['result']);
                    modal.close();
                };
            });
        </script>
        """
    )
