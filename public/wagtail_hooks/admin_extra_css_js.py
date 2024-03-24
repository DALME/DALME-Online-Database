"""Add extra css and javascript to admin."""

from django.templatetags.static import static
from django.utils.html import format_html


def extra_admin_css():
    return format_html(
        '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.14.0/css/all.min.css" integrity="sha512-1PKOgIY59xJ8Co8+NE6FZ+LOAZKjy+KY8iq0G4B3CyeY6wYHN3yt9PW0XpSriVlkMXe40PTKnXrLnZ9+fkDaog==" crossorigin="anonymous" /> \
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/selectize.js/0.12.6/css/selectize.default.min.css" integrity="sha256-ibvTNlNAB4VMqE5uFlnBME6hlparj5sEr1ovZ3B/bNA=" crossorigin="anonymous" /> \
        <link rel="stylesheet" href="{}">',
        static('css/public_admin.css'),
    )


def extra_admin_js():
    return format_html(
        '<script type="text/javascript" src="https://cdn.jsdelivr.net/npm/snarkdown@2.0.0/dist/snarkdown.umd.js" integrity="sha256-QqCCWG2y306e9DZ9VbcdrkacMAz1nubFmYCkac3I3AM=" crossorigin="anonymous"></script> \
        <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/selectize.js/0.12.6/js/standalone/selectize.min.js" integrity="sha256-+C0A5Ilqmu4QcSPxrlGpaZxJ04VjsRjKu+G82kl5UJk=" crossorigin="anonymous"></script> \
        <script type="text/javascript" src="https://cdn.jsdelivr.net/npm/citation-js@0.4.10/build/citation.min.js" integrity="sha256-vqUHuIyFzuc0osFFLRQk5hhFPLGHSnc4jvAtp9lZYvo=" crossorigin="anonymous"></script> \
        <script type="text/javascript" src="{}"></script>\
        <script type="text/javascript" src="{}"></script>\
        <script type="text/javascript" src="{}"></script>',
        static('js/bootstrap-markdown.js'),
        static('js/common_utilities.js'),
        static('js/wagtail_admin_addons.js'),
    )
