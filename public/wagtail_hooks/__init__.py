"""Interface for the public.wagtail_hooks module."""

from wagtail import hooks

from public.extensions.bibliography import (
    BiblioChooserViewSet,
    BiblioViewSet,
    ReferenceChooserViewSet,
    add_reference_js_to_editor,
    register_reference_feature,
)

# from public.extensions.footnotes import add_footnotes_js_to_editor, enable_footnotes
from public.extensions.gradients import GradientChooserViewSet, GradientViewSet, add_gradients_js_to_editor
from public.extensions.saved_searches import add_savedsearch_js_to_editor

from .admin_extra_css_js import extra_admin_css, extra_admin_js
from .editor_extra_js import add_extra_js_to_editor
from .hide_users_menu import hide_users_menu
from .link_converter_rule import link_converter_rule
from .redirects_before_serving import add_redirects_before_serving_pages
from .rich_text_features import enable_rich_text_features

hooks.register('construct_settings_menu', hide_users_menu)
hooks.register('insert_global_admin_css', extra_admin_css, order=0)
hooks.register('insert_global_admin_js', extra_admin_js)
hooks.register('before_serve_page', add_redirects_before_serving_pages)
hooks.register('insert_editor_js', add_extra_js_to_editor)
hooks.register('insert_editor_js', add_gradients_js_to_editor)
hooks.register('insert_editor_js', add_reference_js_to_editor)
# hooks.register('insert_editor_js', add_footnotes_js_to_editor)
hooks.register('insert_editor_js', add_savedsearch_js_to_editor)
hooks.register('register_rich_text_features', link_converter_rule)
# hooks.register('register_rich_text_features', enable_footnotes)
hooks.register('register_rich_text_features', enable_rich_text_features)
hooks.register('register_admin_viewset', GradientViewSet)
hooks.register('register_admin_viewset', GradientChooserViewSet)
hooks.register('register_admin_viewset', BiblioViewSet)
hooks.register('register_admin_viewset', BiblioChooserViewSet)
hooks.register('register_admin_viewset', ReferenceChooserViewSet)
hooks.register('register_rich_text_features', register_reference_feature)
