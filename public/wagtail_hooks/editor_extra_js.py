"""Add additional javascript to editor."""

from django.urls import reverse
from django.utils.html import format_html


def add_extra_js_to_editor():
    return format_html(
        """
            <script type="text/javascript">
                window.chooserUrls['pageChooser'] = '{}';
            </script>
            """,
        reverse('wagtailadmin_chooser_page_reroute'),
    )
