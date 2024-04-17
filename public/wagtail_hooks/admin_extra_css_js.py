"""Add extra css and javascript to admin."""

from django.conf import settings
from django.templatetags.static import static
from django.utils.html import format_html


def extra_admin_css():
    return format_html(
        '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.14.0/css/all.min.css" integrity="sha512-1PKOgIY59xJ8Co8+NE6FZ+LOAZKjy+KY8iq0G4B3CyeY6wYHN3yt9PW0XpSriVlkMXe40PTKnXrLnZ9+fkDaog==" crossorigin="anonymous" /> \
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.13/css/select2.min.css" integrity="sha512-nMNlpuaDPrqlEls3IX/Q56H36qvBASwb3ipuo3MxeWbsQB1881ox0cRv7UPTgBlriqoynt35KjEwgGUeUXIPnw==" crossorigin="anonymous" referrerpolicy="no-referrer" /> \
        <link rel="stylesheet" href="{}">',
        static('css/public_admin.css'),
    )


def extra_admin_js():
    return format_html(
        '<script type="text/javascript" src="https://cdn.jsdelivr.net/npm/citation-js@0.4.10/build/citation.min.js" integrity="sha256-vqUHuIyFzuc0osFFLRQk5hhFPLGHSnc4jvAtp9lZYvo=" crossorigin="anonymous"></script> \
        <script src="https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.13/js/select2.full.min.js" integrity="sha512-RtZU3AyMVArmHLiW0suEZ9McadTdegwbgtiQl5Qqo9kunkVg1ofwueXD8/8wv3Af8jkME3DDe3yLfR8HSJfT2g==" crossorigin="anonymous" referrerpolicy="no-referrer"></script> \
        <script type="text/javascript">window.cite = require("citation-js")</script>\
        <script type="text/javascript" src="{}"></script>\
        <script type="text/javascript" src="{}"></script>\
        <script type="text/javascript">window.APIURL = "{}"</script>',
        static('js/wagtailUtils.js'),
        static('js/wagtailStartup.js'),
        settings.API_URL,
    )
