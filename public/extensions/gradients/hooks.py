"""Hooks for gradients extension."""

from django.urls import reverse
from django.utils.html import format_html


def add_gradients_js_to_editor():
    return format_html(
        """
            <script type="text/javascript">
                window.chooserUrls.gradientChooser = '{}';
            </script>
            """,
        reverse('gradient_chooser:choose'),
    )
