"""Add extra css and javascript to admin."""

from django.conf import settings
from django.templatetags.static import static
from django.utils.html import format_html


def extra_admin_css():
    return format_html(
        '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.14.0/css/all.min.css" integrity="sha512-1PKOgIY59xJ8Co8+NE6FZ+LOAZKjy+KY8iq0G4B3CyeY6wYHN3yt9PW0XpSriVlkMXe40PTKnXrLnZ9+fkDaog==" crossorigin="anonymous" /> \
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css" integrity="sha256-zaSoHBhwFdle0scfGEFUCwggPN7F+ip9XRglo8IWb4w=" crossorigin="anonymous"> \
        <link rel="stylesheet" href="{}">',
        static('web/css/admin.css'),
    )


def extra_admin_js():
    return format_html(
        '<script type="text/javascript" src="https://cdn.jsdelivr.net/npm/citation-js@0.4.10/build/citation.min.js" integrity="sha256-vqUHuIyFzuc0osFFLRQk5hhFPLGHSnc4jvAtp9lZYvo=" crossorigin="anonymous"></script> \
        <script src="https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.full.min.js" integrity="sha256-gtZlnMWqbrBdDWvmCQCgfiA3kq8J4FMqQ4a8Tvmgopk=" crossorigin="anonymous"></script> \
        <script type="text/javascript">window.cite = require("citation-js")</script>\
        <script type="text/javascript" src="{}"></script>\
        <script type="text/javascript" src="{}"></script>\
        <script type="text/javascript">window.APIURL = "{}"</script>',
        static('web/js/wagtailUtils.js'),
        static('web/js/wagtailAdminStartup.js'),
        settings.API_URL,
    )
