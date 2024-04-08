"""Hooks for saved searches extension."""

from wagtail import hooks

from django.urls import reverse
from django.utils.html import format_html


@hooks.register('insert_editor_js')
def add_savedsearch_js_to_editor():
    return (
        format_html(
            """
            <script type="text/javascript">
                window.chooserUrls['savedSearchChooser'] = '{}';
            </script>
            """,
            reverse('wagtailadmin_choose_saved_search'),
        )
        + """
            <script type="text/javascript">
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
    )
