"""Hooks for gradients extension."""

from wagtail import hooks

from django.templatetags.static import static
from django.urls import reverse
from django.utils.html import format_html

from .views import GradientChooserViewSet, GradientViewSet

hooks.register('register_admin_viewset', GradientViewSet)
hooks.register('register_admin_viewset', GradientChooserViewSet)


@hooks.register('insert_editor_js')
def add_gradients_js_to_editor():
    return format_html(
        """
            <script type="text/javascript">
                window.chooserUrls.gradientChooser = '{}';
            </script>
            """,
        reverse('gradient_chooser:choose'),
    )


@hooks.register('insert_global_admin_css')
def extra_admin_css():
    return format_html('<link rel="stylesheet" href="{}">', static('css/gradient-chooser.css'))
