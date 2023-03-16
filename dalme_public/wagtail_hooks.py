"""Define hooks for wagtail."""
import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail import hooks
from wagtail.admin.rich_text.converters.html_to_contentstate import (
    ExternalLinkElementHandler,
    PageLinkElementHandler,
)

from django.shortcuts import redirect
from django.templatetags.static import static
from django.urls import reverse
from django.utils.html import format_html

from dalme_public.handlers import (
    BibliographyElementHandler,
    BibliographyLinkHandler,
    FootnoteElementHandler,
    SavedSearchElementHandler,
    SavedSearchLinkHandler,
    footnote_decorator,
    link_entity_decorator,
)


@hooks.register('construct_settings_menu')
def hide_users_menu_item(request, menu_items):  # noqa: ARG001
    menu_items[:] = [item for item in menu_items if item.name not in ['users', 'groups']]


@hooks.register('insert_global_admin_css', order=0)
def extra_admin_css():
    return format_html('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.14.0/css/all.min.css" integrity="sha512-1PKOgIY59xJ8Co8+NE6FZ+LOAZKjy+KY8iq0G4B3CyeY6wYHN3yt9PW0XpSriVlkMXe40PTKnXrLnZ9+fkDaog==" crossorigin="anonymous" /> \
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/selectize.js/0.12.6/css/selectize.default.min.css" integrity="sha256-ibvTNlNAB4VMqE5uFlnBME6hlparj5sEr1ovZ3B/bNA=" crossorigin="anonymous" /> \
        <link rel="stylesheet" href="{}">', static("css/dalme_public/dalme_public_admin.css"))


@hooks.register('insert_global_admin_js')
def global_admin_js():
    return format_html('<script src="https://cdn.jsdelivr.net/npm/snarkdown@2.0.0/dist/snarkdown.umd.js" integrity="sha256-QqCCWG2y306e9DZ9VbcdrkacMAz1nubFmYCkac3I3AM=" crossorigin="anonymous"></script> \
        <script src="https://cdnjs.cloudflare.com/ajax/libs/selectize.js/0.12.6/js/standalone/selectize.min.js" integrity="sha256-+C0A5Ilqmu4QcSPxrlGpaZxJ04VjsRjKu+G82kl5UJk=" crossorigin="anonymous"></script> \
        <script src="https://cdn.jsdelivr.net/npm/citation-js@0.4.10/build/citation.min.js" integrity="sha256-vqUHuIyFzuc0osFFLRQk5hhFPLGHSnc4jvAtp9lZYvo=" crossorigin="anonymous"></script> \
        <script src="{}"></script><script src="{}"></script><script src="{}"></script>', static("js/bootstrap-markdown.js"), static("js/dalme_app/dalme_util.js"), static("js/wagtail_admin_addons.js"))


@hooks.register('before_serve_page')
def redirects(page, request, serve_args, serve_kwargs):  # noqa: ARG001
    if page.is_root():
        home = page.get_children().live().first()
        return redirect(home.url, permanent=False)

    if page._meta.label == 'dalme_public.Section':  # noqa: SLF001
        url = page.get_children().live().first().url
        return redirect(url, permanent=False)

    return None


@hooks.register('insert_editor_js')
def editor_js():
    return format_html(
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


@hooks.register('register_rich_text_features')
def register_add_ons(features):
    del features.converter_rules_by_converter['contentstate']['link']
    features.register_converter_rule('contentstate', 'link', {
        'from_database_format': {
            'a[href]': ExternalLinkElementHandler('LINK'),
            'a[linktype="page"]': PageLinkElementHandler('LINK'),
            'a[linktype="saved_search"]': SavedSearchElementHandler('LINK'),
            'a[linktype="biblio_entry"]': BibliographyElementHandler('LINK'),
        },
        'to_database_format': {
            'entity_decorators': {'LINK': link_entity_decorator},
        },
    })
    features.register_link_type(SavedSearchLinkHandler)
    features.register_link_type(BibliographyLinkHandler)


@hooks.register('register_rich_text_features')
def register_footnote(features):
    features.default_features.append('footnote')
    feature_name = 'footnote'
    type_ = 'FOOTNOTE'

    control = {
        'type': type_,
        'icon': [
            "M917.5,83.3c0-10.7-10.3-19.4-23-19.4H123.7c-12.7,0-23,8.7-23,19.4v854.4c0,10.7,10.3,19.4,23,19.4h770.8c12.7,0,23-8.7,23-19.4L917.5,83.3L917.5,83.3z",
            "M962.1,84.4c0-32.2-30.8-58.3-68.9-58.3H125.1c-38.1,0-68.9,26.1-68.9,58.3v854.5c0,32.2,30.9,58.3,68.9,58.3h768.1c38.1,0,68.9-26.1,68.9-58.3L962.1,84.4L962.1,84.4z M884.1,907.3c0,9.9-9.5,17.9-21.2,17.9H151.1c-11.7,0-21.2-8-21.2-17.9v-789c0-9.9,9.5-17.9,21.2-17.9h711.8c11.7,0,21.2,8,21.2,17.9L884.1,907.3L884.1,907.3z",
            "M429.9,420.5h360.4v70H429.9V420.5z M223.7,530.3h566.6v70H223.7V530.3z M223.7,642.5h566.6v70H223.7V642.5z M223.7,753.3h566.6v70H223.7V753.3z M268.4,182.4h117.3v306.8H268.4V182.4z M225.8,285.1h42.5v-64.8h-42.5V285.1z",
        ],
        'description': 'Insert footnote',
    }

    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.EntityFeature(
            control,
            js=['js/dalme_public_footnote.js'],
            css={'all': ['css/dalme_public/dalme_public_footnote.css']},
        ),
    )

    features.register_converter_rule('contentstate', feature_name, {
        'from_database_format': {'span[data-footnote]': FootnoteElementHandler(type_)},
        'to_database_format': {'entity_decorators': {type_: footnote_decorator}},
    })
