"""Interface for the public.wagtail_hooks module."""

from wagtail import hooks
from wagtail.snippets.models import register_snippet

from .add_extra_css_js_to_admin import extra_admin_css, extra_admin_js
from .add_extra_js_to_editor import add_extra_js_to_editor
from .add_redirects_before_serving_pages import add_redirects_before_serving_pages
from .enable_footnotes import enable_footnotes
from .enable_rich_text_features import enable_rich_text_features
from .enable_savedsearch_biblio import enable_savedsearch_biblio
from .gradients import GradientViewSet
from .hide_settings_users_menu_item import hide_settings_users_menu_item

hooks.register('construct_settings_menu', hide_settings_users_menu_item)
hooks.register('insert_global_admin_css', extra_admin_css, order=0)
hooks.register('insert_global_admin_js', extra_admin_js)
hooks.register('before_serve_page', add_redirects_before_serving_pages)
hooks.register('insert_editor_js', add_extra_js_to_editor)
hooks.register('register_rich_text_features', enable_savedsearch_biblio)
hooks.register('register_rich_text_features', enable_footnotes)
hooks.register('register_rich_text_features', enable_rich_text_features)

register_snippet(GradientViewSet)
